# Добавление навигации

Это руководство основывается на первом шаге учебника "Начало работы с базовым приложением Angular" (начните "Начало работы с базовым приложением Angular").

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

In this case, the route, or URL, contains one fixed segment, `/products`.

The final segment is variable, inserting the `id` property of the current product.

For example, the URL for a product with an `id` of 1 would be similar to `https://getting-started-myfork.stackblitz.io/products/1`.

**5.** Verify that the router works as intended by clicking the product name.

The application should display the `ProductDetailsComponent`, which currently says "product-details works!"

Notice that the URL in the preview window changes.

The final segment is `products/#` where `#` is the number of the route you clicked.

![Product details view with updated URL](product-details-works.png)

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

**4.** In the `ngOnInit()` method, extract the `productId` from the route parameters and find the corresponding product in the `products` array.

```ts
ngOnInit() {
  // First get the product id from the current route.
  const routeParams = this.route.snapshot.paramMap;
  const productIdFromRoute = Number(routeParams.get('productId'));

  // Find the product that correspond with the id provided in route.
  this.product = products.find(product => product.id === productIdFromRoute);
}
```

The route parameters correspond to the path variables you define in the route.

To access the route parameters, we use `route.snapshot`, which is the `ActivatedRouteSnapshot` that contains information about the active route at that particular moment in time.

The URL that matches the route provides the `productId` .

Angular uses the `productId` to display the details for each unique product.

**5.** Update the `ProductDetailsComponent` template to display product details with an `*ngIf`.

If a product exists, the `<div>` renders with a name, price, and description.

```html
<h2>Product Details</h2>

<div *ngIf="product">
    <h3>{{ product.name }}</h3>
    <h4>{{ product.price | currency }}</h4>
    <p>{{ product.description }}</p>
</div>
```

Строка `<h4>{{ product.price | currency }}</h4>` использует трубу `currency` для преобразования `product.price` из числа в строку валюты.

`Pipe` - это способ преобразования данных в шаблоне HTML.

Для получения дополнительной информации о трубах Angular смотрите [Pipes](pipes.md).

---

Когда пользователи нажимают на название в списке продуктов, маршрутизатор переводит их на отдельный URL-адрес продукта, показывает компонент `ProductDetailsComponent` и отображает подробную информацию о продукте.

![Product details page with updated URL and full details displayed](product-details-routed.png)

Для получения дополнительной информации о маршрутизаторе Angular Router смотрите [Маршрутизация и навигация](router.md).

## Что дальше

Вы настроили свое приложение так, чтобы можно было просматривать подробную информацию о товарах, каждый из которых имеет свой URL.

Чтобы продолжить знакомство с Angular:

-   Перейдите к разделу [Управление данными](start-data.md), чтобы добавить функцию корзины, управлять данными корзины и получать внешние данные для цен доставки.
-   Перейдите к [Deployment](start-deployment.md), чтобы развернуть ваше приложение на Firebase или перейти к локальной разработке.
