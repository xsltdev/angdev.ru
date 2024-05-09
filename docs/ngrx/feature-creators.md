---
description: Feature Creators это функции, которые позволяют создавать редьюсеры и селекторы для управления глобальным состоянием в Angular приложении с использованием NgRx
---

# Feature Creators

## Что такое Ngrx Feature?

В @ngrx/store есть три основных строительных блока для управления глобальным состоянием: [действия](actions.md), [редьюсеры](reducers.md) и [селекторы](selectors.md). Для конкретного `feature` хранилища мы создаем редьюсер `reducer` для обработки смены состояния хранилища (которое вызывается с помощью действий `actions`) и селекторов `selectors` для получения фрагментов `feature` хранилища. Также нам нужно определить название (ключ) `name` редьюсера, необходимое для регистрации `feature` редьюсера в хранилище NgRx. Таким образом, мы можем рассматривать `feature NgRx` как объединение имени редьюсера, функции редьюсера и селекторов для конкретного состояния редьюсера.

## Использование Feature Creators

Функция `createFeature` сокращает количество повторяющихся селекторов в коде, автоматически генерируя селектор хранилища и дочерние селекторы для каждого свойства состояния хранилища. В качестве входного аргумента она принимает объект, содержащий имя и редьюсер:

_books.reducer.ts_

```ts
import { createFeature, createReducer, on } from '@ngrx/store';
import { Book } from './book.model';

import * as BookListPageActions from './book-list-page.actions';
import * as BooksApiActions from './books-api.actions';

interface State {
    books: Book[];
    loading: boolean;
}

const initialState: State = {
    books: [],
    loading: false,
};

export const booksFeature = createFeature({
    name: 'books',
    reducer: createReducer(
        initialState,
        on(BookListPageActions.enter, (state) => ({
            ...state,
            loading: true,
        })),
        on(BooksApiActions.loadBooksSuccess, (state, { books }) => ({
            ...state,
            books,
            loading: false,
        })),
    ),
});

export const { 
    name, // название хранилища
    reducer, // редьюсер хранлища
    selectBooksState, // селектор для всего хранлища
    selectBooks, // селектор для свойства `books`
    selectLoading, // селектор для свойства `loading`
} = booksFeature;
```

Объект, созданный с помощью функции `createFeature`, содержит имя, редьюсер, селектор всего хранилища и селектор для каждого свойства состояния хранилища. Все созданные селекторы имеют префикс `select`, а селектор хранилища - суффикс `State`. В этом примере имя селектора для хранилища - `selectBooksState`, где `books` - имя свойства. Имена дочерних селекторов - `selectBooks` и `selectLoading` - основаны на именах свойств состояния хранилища `books`.

Созданные селекторы можно использовать как самостоятельно, так и для создания других селекторов:

_books.selectors.ts_

```ts
import { createSelector } from '@ngrx/store';
import { booksFeature } from './books.reducer';

export const selectBookListPageViewModel = createSelector(
    booksFeature.selectBooks,
    booksFeature.selectLoading,
    (books, loading) => ({ books, loading })
);
```
## Дополнительные селекторы

Функция `createFeature` так же может быть использована для предоставления дополнительных селекторов для состояния хранилища с помощью опционального метода `extraSelectors`:

_books.feature.ts_

```ts
import { createFeature, createReducer, on } from '@ngrx/store';
import { Book } from './book.model';

import * as BookListPageActions from './book-list-page.actions';

interface State {
    books: Book[];
    query: string;
}

const initialState: State = {
    books: [],
    query: '',
};

export const booksFeature = createFeature({
    name: 'books',
    reducer: createReducer(
        initialState,
        on(BookListPageActions.search, (state, action) => ({
            ...state,
            query: action.query,
        })),
    ),
    extraSelectors: ({ selectQuery, selectBooks }) => ({
        selectFilteredBooks: createSelector(
            selectQuery,
            selectBooks,
            (query, books) => books.filter(book => book.title.includes(query)),
        ),
    }),
});
```

Метод `extraSelectors` это функция, которая принимает селекторы в качестве входных аргументов и возвращает объект со всеми дополнительными селекторами. Мы можем добавлять столько дополнительных селекторов, сколько нам нужно.

### Повторное использование дополнительных селекторов

Повторное использование дополнительных селекторов можно сделать следующим образом:

_books.feature.ts_

```ts
import { createFeature, createReducer, on } from '@ngrx/store';
import { Book } from './book.model';

import * as BookListPageActions from './book-list-page.actions';

interface State {
    books: Book[];
    query: string;
}

const initialState: State = {
    books: [],
    query: '',
};

export const booksFeature = createFeature({
    name: 'books',
    reducer: createReducer(
        initialState,
            on(BookListPageActions.search, (state, action) => ({
                ...state,
            query: action.query,
        }))
    ),
    extraSelectors: ({ selectQuery, selectBooks }) => {
        const selectFilteredBooks = createSelector(
              selectQuery,
              selectBooks,
              (query, books) => books.filter((book) => book.title.includes(query))
        );
        const selectFilteredBooksWithRating = createSelector(
              selectFilteredBooks,
              (books) => books.filter((book) => book.ratingsCount >= 1)
        );

        return { selectFilteredBooks, selectFilteredBooksWithRating };
    },
});
```

## Регистрация Ngrx Feature

Регистрация `feature` хранилища в глобальном состоянии может быть выполнена путем передачи как аргумента всего объекта `feature` в метод `StoreModule.forFeature`:

_books.module.ts_ 

```ts
import { NgModule } from '@angular/core';
import { StoreModule } from '@ngrx/store';

import { booksFeature } from './books.reducer';

@NgModule({
    imports: [StoreModule.forFeature(booksFeature)],
})
export class BooksModule {}
```

### Использование Standalone API

Регистрация хранилища может быть выполнена с помощью Standalone API, если вы работаете с Angular в режиме `Standalone`.

_main.ts_

```ts
import { bootstrapApplication } from '@angular/platform-browser';
import { provideStore, provideState } from '@ngrx/store';

import { AppComponent } from './app.component';
import { booksFeature } from './books.reducer';

bootstrapApplication(AppComponent, {
	providers: [
		provideStore(),
		provideState(booksFeature)
	],
});
```

`Feature` хранилища также могут быть зарегистрированы в массиве `providers` в конфигурации роутера.

_books-routes.ts_

```ts
import { Route } from '@angular/router';
import { provideState } from '@ngrx/store';

import { booksFeature } from './books.reducer';

export const routes: Route[] = [
	{
        path: 'books',
        providers: [
            provideState(booksFeature)
        ]
	}
];
```

## Ограничения
 
Функция `createFeature` не может быть использована для функций, состояние которых содержит необязательные свойства. Другими словами, все свойства состояния должны быть переданы в начальный объект состояния.

Если состояние содержит необязательные свойства:

_books.reducer.ts_

```ts
interface State {
    books: Book[];
    activeBookId?: string;
}

const initialState: State = {
    books: [],
};
```

Каждый необязательный символ (?) должен быть заменен на `| null` или `| undefined`:

_books.reducer.ts_

```ts
interface State {
    books: Book[];
    activeBookId: string | null;
    // или activeBookId: string | undefined;
}

const initialState: State = {
    books: [],
    activeBookId: null,
    // или activeBookId: undefined,
};
```

## Ссылки

- [Angular NgRx - How to use Feature Creator (Video)](https://www.youtube.com/watch?v=bHw8SV4SNUU)
- [NgRx Feature Creator | ng- conf 2022 (Video)](https://www.youtube.com/watch?v=t69Hj1V9DuEs)
