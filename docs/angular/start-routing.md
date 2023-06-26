# Добавление навигации

Это руководство основывается на первом шаге учебника "[Начало работы с базовым приложением Angular](start.md)".

На данном этапе разработки приложение интернет-магазина имеет базовый каталог товаров.

В следующих разделах вы добавите в приложение следующие функции:

-   Введите URL-адрес в адресной строке, чтобы перейти на соответствующую страницу товара.
-   Щелкайте по ссылкам на странице для навигации внутри вашего одностраничного приложения
-   Нажимайте кнопки браузера "назад" и "вперед" для интуитивной навигации по истории браузера.

## Ассоциируйте URL-путь с компонентом

Приложение уже использует Angular `Router` для перехода к компоненту `ProductListComponent`. В этом разделе показано, как определить маршрут для отображения отдельных деталей продукта.

**1.** Создайте новый компонент для подробной информации о продукте.

В терминале создайте новый компонент `product-details`, выполнив следующую команду:

```console
ng generate component product-details
```

**2.** В `app.module.ts` добавьте маршрут для деталей продукта, с `путем` `products/:productId` и `ProductDetailsComponent` для `компонента`.

```ts
@NgModule({
  imports: [
    BrowserModule,
    ReactiveFormsModule,
    RouterModule.forRoot([
      { path: '', component: ProductListComponent },
      { path: 'products/:productId', component: ProductDetailsComponent },
    ])
  ],
  declarations: [
    AppComponent,
    TopBarComponent,
    ProductListComponent,
    ProductAlertsComponent,
    ProductDetailsComponent,
  ],
})
```

**3.** Откройте `product-list.component.html`.

**4.** Измените якорь названия продукта, чтобы включить `routerLink` с `product.id` в качестве параметра.

```html
<div *ngFor="let product of products">
    <h3>
        <a
            [title]="product.name + ' details'"
            [routerLink]="['/products', product.id]"
        >
            {{ product.name }}
        </a>
    </h3>

    <!-- . . . -->
</div>
```

Директива `RouterLink` помогает вам настроить элемент якоря.

В данном случае маршрут, или URL, содержит один фиксированный сегмент, `/products`.

Последний сегмент является переменным и вставляет свойство `id` текущего продукта.

Например, URL для продукта с `id`, равным 1, будет выглядеть так: `https://getting-started-myfork.stackblitz.io/products/1`.

**5.** Убедитесь, что маршрутизатор работает так, как задумано, щелкнув по названию продукта.

Приложение должно отобразить `ProductDetailsComponent`, который в настоящее время говорит "product-details works!".

Обратите внимание, что URL в окне предварительного просмотра меняется.

Конечным сегментом является `products/#`, где `#` - это номер маршрута, на который вы нажали.

![Просмотр сведений о продукте с обновленным URL](product-details-works.png)

## Просмотр информации о продукте

Компонент `ProductDetailsComponent` управляет отображением каждого продукта. Angular Router отображает компоненты на основе URL браузера и определенных вами маршрутов.

В этом разделе вы будете использовать Angular Router для объединения данных `products` и информации о маршрутах, чтобы отобразить конкретные детали для каждого продукта.

**1.** В `product-details.component.ts` импортируйте `ActivatedRoute` из `@angular/router`, а массив `products` из `../products`.

```ts
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { Product, products } from '../products';
```

**2.** Определите свойство `product`.

```ts
export class ProductDetailsComponent implements OnInit {
    product: Product | undefined;
    /* ... */
}
```

**3.** Вставьте `ActivatedRoute` в `constructor()`, добавив `private route: ActivatedRoute` в качестве аргумента в круглых скобках конструктора.

```ts
export class ProductDetailsComponent implements OnInit {
    product: Product | undefined;

    constructor(private route: ActivatedRoute) {}
}
```

`ActivatedRoute` специфичен для каждого компонента, который загружает Angular Router.

`ActivatedRoute` содержит информацию о маршруте и параметрах маршрута.

Внедряя `ActivatedRoute`, вы настраиваете компонент на использование сервиса.

Шаг [Управление данными](start-data.md) более подробно рассматривает сервисы.

**4.** В методе `ngOnInit()` извлеките `productId` из параметров маршрута и найдите соответствующий продукт в массиве `products`.

```ts
ngOnInit() {
  // First get the product id from the current route.
  const routeParams = this.route.snapshot.paramMap;
  const productIdFromRoute = Number(routeParams.get('productId'));

  // Find the product that correspond with the id provided in route.
  this.product = products.find(
	product => product.id === productIdFromRoute
  );
}
```

Параметры маршрута соответствуют переменным пути, которые вы определяете в маршруте.

Для доступа к параметрам маршрута используется `route.snapshot`, который представляет собой `ActivatedRouteSnapshot`, содержащий информацию об активном маршруте в данный момент времени.

URL, соответствующий маршруту, содержит `productId`.

Angular использует `productId` для отображения подробностей о каждом уникальном продукте.

**5.** Обновите шаблон `ProductDetailsComponent` для отображения информации о товаре с помощью `*ngIf`.

Если товар существует, `<div>` отображается с названием, ценой и описанием.

```html
<h2>Product Details</h2>

<div *ngIf="product">
    <h3>{{ product.name }}</h3>
    <h4>{{ product.price | currency }}</h4>
    <p>{{ product.description }}</p>
</div>
```

Строка `<h4>{{ product.price | currency }}</h4>` использует пайп `currency` для преобразования `product.price` из числа в строку валюты.

`Pipe` — это способ преобразования данных в шаблоне HTML.

Для получения дополнительной информации о пайпах Angular смотрите [Пайпы](pipes.md).

Когда пользователи нажимают на название в списке продуктов, маршрутизатор переводит их на отдельный URL-адрес продукта, показывает компонент `ProductDetailsComponent` и отображает подробную информацию о продукте.

![Страница подробной информации о продукте с обновленным URL и отображением полной информации](product-details-routed.png)

Для получения дополнительной информации о маршрутизаторе Angular Router смотрите [Маршрутизация и навигация](router.md).

## Что дальше

Вы настроили свое приложение так, чтобы можно было просматривать подробную информацию о товарах, каждый из которых имеет свой URL.

Чтобы продолжить знакомство с Angular:

-   Перейдите к разделу [Управление данными](start-data.md), чтобы добавить функцию корзины, управлять данными корзины и получать внешние данные для цен доставки.
-   Перейдите к [Развертывание](start-deployment.md), чтобы развернуть ваше приложение на Firebase или перейти к локальной разработке.

:date: 28.02.2022
