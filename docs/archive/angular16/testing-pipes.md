# Тестирование пайпов

:date: 28.02.2022

Вы можете протестировать [pipes](pipes.md) без использования утилит тестирования Angular.

!!!note ""

    Если вы хотите поэкспериментировать с приложением, которое описано в этом руководстве, [запустите его в браузере](https://angular.io/generated/live-examples/testing/stackblitz.html) или скачайте и запустите его локально.

## Тестирование `TitleCasePipe`

Класс pipe имеет один метод, `transform`, который манипулирует входным значением в преобразованное выходное значение. Реализация `transform` редко взаимодействует с DOM.

Большинство пайпов не зависят от Angular, кроме метаданных `@Pipe` и интерфейса.

Рассмотрим `TitleCasePipe`, который выводит первую букву каждого слова. Вот реализация с регулярным выражением.

```ts
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'titlecase', pure: true })
/** Transform to Title Case: uppercase the first letter of the words in a string. */
export class TitleCasePipe implements PipeTransform {
    transform(input: string): string {
        return input.length === 0
            ? ''
            : input.replace(
                  /\w\S*/g,
                  (txt) =>
                      txt[0].toUpperCase() +
                      txt.slice(1).toLowerCase()
              );
    }
}
```

Все, что использует регулярное выражение, стоит тщательно протестировать. Используйте простой Jasmine для изучения ожидаемых и побочных случаев.

```ts
describe('TitleCasePipe', () => {
    // This pipe is a pure, stateless function so no need for BeforeEach
    const pipe = new TitleCasePipe();

    it('transforms "abc" to "Abc"', () => {
        expect(pipe.transform('abc')).toBe('Abc');
    });

    it('transforms "abc def" to "Abc Def"', () => {
        expect(pipe.transform('abc def')).toBe('Abc Def');
    });

    // ... more tests ...
});
```

## Написание тестов DOM для поддержки теста пайпы {: #write-tests}

Это тесты пайпа _в изоляции_. Они не могут определить, правильно ли работает `TitleCasePipe` в компонентах приложения.

Рассмотрите возможность добавления тестов компонентов, таких как этот:

```ts
it('should convert hero name to Title Case', () => {
    // get the name's input and display elements from the DOM
    const hostElement: HTMLElement = harness.routeNativeElement!;
    const nameInput: HTMLInputElement = hostElement.querySelector(
        'input'
    )!;
    const nameDisplay: HTMLElement = hostElement.querySelector(
        'span'
    )!;

    // simulate user entering a new name into the input box
    nameInput.value = 'quick BROWN  fOx';

    // Dispatch a DOM event so that Angular learns of input value change.
    nameInput.dispatchEvent(new Event('input'));

    // Tell Angular to update the display binding through the title pipe
    harness.detectChanges();

    expect(nameDisplay.textContent).toBe(
        'Quick Brown  Fox'
    );
});
```
