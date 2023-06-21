# Управление данными

Это руководство основано на втором этапе руководства [Начало работы с базовым приложением Angular](start.md), [Добавление навигации](start-routing.md). На данном этапе разработки приложение магазина имеет каталог товаров с двумя представлениями: список товаров и подробная информация о товарах.

Пользователи могут нажать на название товара из списка, чтобы увидеть подробности в новом представлении с отдельным URL-адресом или маршрутом.

Этот шаг руководства поможет вам создать корзину для покупок на следующих этапах:

-   Обновите представление подробностей о продукте, чтобы включить кнопку **Купить**, которая добавляет текущий продукт в список продуктов, которыми управляет служба корзины.
-   Добавьте компонент корзины, который отображает товары в корзине.
-   Добавление компонента доставки, который извлекает цены доставки для товаров в корзине, используя `HttpClient` от Angular для получения данных о доставке из файла `.json`.

## Создайте сервис корзины

В Angular сервис - это экземпляр класса, который вы можете сделать доступным для любой части вашего приложения, используя [систему инъекции зависимостей](glossary.md#dependency-injection-di).

В настоящее время пользователи могут просматривать информацию о продукте, а приложение может имитировать обмен информацией и уведомления об изменениях продукта.

Следующим шагом будет создание способа добавления товаров в корзину. В этом разделе мы рассмотрим добавление кнопки **Купить** и настройку службы корзины для хранения информации о товарах в корзине.

### Определение сервиса корзины

В этом разделе мы рассмотрим создание `CartService`, который отслеживает товары, добавленные в корзину.

**1.** В терминале создайте новый сервис `cart`, выполнив следующую команду:

```console
ng generate service cart
```

**2.** Импортируйте интерфейс `Product` из `./products.ts` в файл `cart.service.ts`, а в классе `CartService` определите свойство `items` для хранения массива текущих товаров в корзине.

```ts
import { Product } from './products';
import { Injectable } from '@angular/core';
/* . . . */
@Injectable({
    providedIn: 'root',
})
export class CartService {
    items: Product[] = [];
    /* . . . */
}
```

**3.** Определите методы для добавления товаров в корзину, возврата товаров из корзины и очистки корзины.

```ts
@Injectable({
    providedIn: 'root',
})
export class CartService {
    items: Product[] = [];
    /* . . . */

    addToCart(product: Product) {
        this.items.push(product);
    }

    getItems() {
        return this.items;
    }

    clearCart() {
        this.items = [];
        return this.items;
    }
    /* . . . */
}
```

-   Метод `addToCart()` добавляет товар в массив `items`.
-   Метод `getItems()` собирает товары, которые пользователи добавляют в корзину, и возвращает каждый товар с его количеством.
-   Метод `clearCart()` возвращает пустой массив товаров, который опустошает корзину.

### Использование сервиса корзины

В этом разделе рассказывается об использовании `CartService` для добавления товара в корзину.

**1.** В `product-details.component.ts` импортируйте сервис корзины.

```ts
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { Product, products } from '../products';
import { CartService } from '../cart.service';
```

**2.** Внедрите сервис cart, добавив его в `constructor()`.

```ts
export class ProductDetailsComponent implements OnInit {
    constructor(
        private route: ActivatedRoute,
        private cartService: CartService
    ) {}
}
```

**3.** Определите метод `addToCart()`, который добавляет текущий товар в корзину.

```ts
export class ProductDetailsComponent implements OnInit {
    addToCart(product: Product) {
        this.cartService.addToCart(product);
        window.alert(
            'Your product has been added to the cart!'
        );
    }
}
```

Метод `addToCart()` делает следующее:

-   Принимает текущий `продукт` в качестве аргумента.
-   Использует метод `CartService` `addToCart()` для добавления товара в корзину
-   Выводит сообщение о том, что вы добавили товар в корзину.

**4.** В `product-details.component.html` добавьте кнопку с надписью **Купить** и привяжите событие `click()` к методу `addToCart()`.

This code updates the product details template with a **Buy** button that adds the current product to the cart.

```html
<h2>Product Details</h2>

<div *ngIf="product">
    <h3>{{ product.name }}</h3>
    <h4>{{ product.price | currency }}</h4>
    <p>{{ product.description }}</p>
    <button type="button" (click)="addToCart(product)">
        Buy
    </button>
</div>
```

**5.** Verify that the new **Buy** button appears as expected by refreshing the application and clicking on a product's name to display its details.

![Display details for selected product with a Buy button](product-details-buy.png)

**6.** Click the **Buy** button to add the product to the stored list of items in the cart and display a confirmation message.

![Display details for selected product with a Buy button](buy-alert.png)

## Создание представления корзины

Чтобы клиенты могли видеть свою корзину, вы можете создать представление корзины в два этапа:

1.  Создайте компонент корзины и настройте маршрутизацию к новому компоненту.
2.  Отображение элементов корзины.

### Настройка компонента корзины

Чтобы создать представление корзины, выполните те же шаги, что и при создании компонента `ProductDetailsComponent`, и настройте маршрутизацию для нового компонента.

**1.** Создайте новый компонент с именем `cart` в терминале, выполнив следующую команду:

```console
ng generate component cart
```

Эта команда сгенерирует файл `cart.component.ts` и связанные с ним файлы шаблонов и стилей.

```ts
import { Component } from '@angular/core';

@Component({
    selector: 'app-cart',
    templateUrl: './cart.component.html',
    styleUrls: ['./cart.component.css'],
})
export class CartComponent {}
```

**2.** Обратите внимание, что вновь созданный `CartComponent` добавлен в `declarations` модуля в `app.module.ts`.

```ts
import { CartComponent } from './cart/cart.component';

@NgModule({
  declarations: [
    AppComponent,
    TopBarComponent,
    ProductListComponent,
    ProductAlertsComponent,
    ProductDetailsComponent,
    CartComponent,
  ],
})
```

**3.** Все еще в `app.module.ts` добавьте маршрут для компонента `CartComponent`, с `путем` `cart`.

```ts
@NgModule({
  imports: [
    BrowserModule,
    ReactiveFormsModule,
    RouterModule.forRoot([
      { path: '', component: ProductListComponent },
      { path: 'products/:productId', component: ProductDetailsComponent },
      { path: 'cart', component: CartComponent },
    ])
  ],
})
```

**4.** Обновите кнопку **Checkout** так, чтобы она маршрутизировалась на URL `/cart`.

В `top-bar.component.html` добавьте директиву `routerLink`, указывающую на `/cart`.

```html
<a routerLink="/cart" class="button fancy-button">
    <em class="material-icons">shopping_cart</em>Checkout
</a>
```

**5.** Verify the new `CartComponent` works as expected by clicking the **Checkout** button.

You can see the "cart works!" default text, and the URL has the pattern `https://getting-started.stackblitz.io/cart`, where `getting-started.stackblitz.io` may be different for your StackBlitz project.

![Display cart view before customizing](cart-works.png)

### Display the cart items

This section shows you how to use the cart service to display the products in the cart.

1.  In `cart.component.ts`, import the `CartService` from the `cart.service.ts` file.

    <code-example header="src/app/cart/cart.component.ts" path="getting-started/src/app/cart/cart.component.2.ts" region="imports"></code-example>

1.  Inject the `CartService` so that the `CartComponent` can use it by adding it to the `constructor()`.

    <code-example header="src/app/cart/cart.component.ts" path="getting-started/src/app/cart/cart.component.2.ts" region="inject-cart"></code-example>

1.  Define the `items` property to store the products in the cart.

    <code-example header="src/app/cart/cart.component.ts" path="getting-started/src/app/cart/cart.component.2.ts" region="items"></code-example>

    This code sets the items using the `CartService` `getItems()` method.

    You defined this method [when you created `cart.service.ts`](#generate-cart-service).

1.  Update the cart template with a header, and use a `<div>` with an `*ngFor` to display each of the cart items with its name and price.

    The resulting `CartComponent` template is as follows.

    <code-example header="src/app/cart/cart.component.html" path="getting-started/src/app/cart/cart.component.2.html" region="prices"></code-example>

1.  Verify that your cart works as expected:

    1.  Click **My Store**.

    1.  Click on a product name to display its details.

    1.  Click **Buy** to add the product to the cart.

    1.  Click **Checkout** to see the cart.

    <div class="lightbox">

    <img alt="Cart view with products added" src="generated/images/guide/start/cart-page-full.png">

    </div>

For more information about services, see [Introduction to Services and Dependency Injection](guide/architecture-services 'Concepts > Intro to Services and DI').

## Retrieve shipping prices

Серверы часто возвращают данные в виде потока. Потоки полезны, поскольку они позволяют легко преобразовывать возвращаемые данные и вносить изменения в способ запроса этих данных.
Angular `HttpClient` - это встроенный способ получения данных из внешних API и предоставления их вашему приложению в виде потока.

В этом разделе показано, как использовать `HttpClient` для получения цен на доставку из внешнего файла.

Приложение, которое StackBlitz создает для этого руководства, поставляется с предопределенными данными о доставке в файле `assets/shipping.json`. Используйте эти данные для добавления цен доставки для товаров в корзине.

<code-example header="src/assets/shipping.json" path="getting-started/src/assets/shipping.json"></code-example>.

### Настройте `AppModule` для использования `HttpClient`.

Чтобы использовать `HttpClient` от Angular, вы должны настроить ваше приложение на использование `HttpClientModule`.

Angular `HttpClientModule` регистрирует провайдеров, необходимых вашему приложению для использования сервиса `HttpClient` в вашем приложении.

1.  В файле `app.module.ts` импортируйте `HttpClientModule` из пакета `@angular/common/http` в верхней части файла вместе с другими импортами.

    Поскольку существует ряд других импортов, в данном фрагменте кода они опущены для краткости.

    Обязательно оставьте существующие импорты на месте.

    <code-example header="src/app/app.module.ts" path="getting-started/src/app/app.module.ts" region="http-client-module-import"></code-example>.

1.  Чтобы глобально зарегистрировать провайдеры Angular `HttpClient`, добавьте `HttpClientModule` в массив `AppModule` `@NgModule()` `imports`.

    <code-example header="src/app/app.module.ts" path="getting-started/src/app/app/app.module.ts" region="http-client-module"></code-example>

### Настройте `CartService` на использование `HttpClient`.

Следующим шагом будет внедрение сервиса `HttpClient` в ваш сервис, чтобы ваше приложение могло получать данные и взаимодействовать с внешними API и ресурсами.

1.  В `cart.service.ts` импортируйте `HttpClient` из пакета `@angular/common/http`.

    <code-example header="src/app/cart.service.ts" path="getting-started/src/app/cart.service.ts" region="import-http"></code-example>.

1.  Вставьте `HttpClient` в `конструктор()` сервиса `CartService`.

    <code-example header="src/app/cart.service.ts" path="getting-started/src/app/cart.service.ts" region="inject-http"></code-example>

### Настройте `CartService` для получения цен доставки

Чтобы получить данные о доставке из файла `shipping.json`, вы можете использовать метод `HttpClient` `get()`.

1.  В `cart.service.ts`, ниже метода `clearCart()`, определите новый метод `getShippingPrices()`, который использует метод `HttpClient` `get()`.

    <code-example header="src/app/cart.service.ts" path="getting-started/src/app/cart.service.ts" region="get-shipping"></code-example>.

Для получения дополнительной информации о `HttpClient` в Angular, смотрите руководство [Client-Server Interaction](guide/http 'Взаимодействие с сервером через HTTP').

## Создание компонента доставки

Теперь, когда вы настроили свое приложение на получение данных о доставке, вы можете создать место для отображения этих данных.

1.  Создайте компонент корзины с именем `shipping` в терминале, выполнив следующую команду:

    <code-example format="shell" language="shell">.

    ng generate component shipping

    </code-example>.

    Эта команда создаст файл `shipping.component.ts` и связанные с ним файлы шаблонов и стилей.

    <code-example header="src/app/shipping/shipping.component.ts" path="getting-started/src/app/shipping/shipping.component.1.ts"></code-example>

1.  В `app.module.ts` добавьте маршрут для доставки.

    Укажите `путь` `shipping` и компонент `ShippingComponent`.

    <code-example header="src/app/app.module.ts" path="getting-started/src/app/app/app.module.ts" region="shipping-route"></code-example>.

    Пока нет ссылки на новый компонент доставки, но вы можете увидеть его шаблон в панели предварительного просмотра, введя URL, указанный в его маршруте.

    URL имеет шаблон: `https://angular-ynqttp--4200.local.webcontainer.io/shipping`, где часть `angular-ynqttp--4200.local.webcontainer.io` может быть другой для вашего проекта StackBlitz.

### Настройка `ShippingComponent` для использования `CartService`.

Этот раздел поможет вам модифицировать `ShippingComponent` для получения данных о доставке по HTTP из файла `shipping.json`.

1.  В `shipping.component.ts` импортируйте `CartService`.

    <code-example header="src/app/shipping/shipping.component.ts" path="getting-started/src/app/shipping/shipping.component.ts" region="imports"></code-example>.

1.  Вставьте сервис корзины в `ShippingComponent` `constructor()`.

    <code-example header="src/app/shipping/shipping.component.ts" path="getting-started/src/app/shipping/shipping.component.ts" region="inject-cart-service"></code-example>.

1.  Определите свойство `shippingCosts`, которое устанавливает свойство `shippingCosts` с помощью метода `getShippingPrices()` из `CartService`.

    Инициализируйте свойство `shippingCosts` в методе `ngOnInit()`.

    <code-example header="src/app/shipping/shipping.component.ts" path="getting-started/src/app/shipping/shipping.component.ts" region="props"></code-example>.

1.  Обновите шаблон `ShippingComponent` для отображения типов доставки и цен с помощью трубы `async`.

    <code-example header="src/app/shipping/shipping.component.html" path="getting-started/src/app/shipping/shipping.component.html"></code-example>.

    Труба `async` возвращает последнее значение из потока данных и продолжает делать это в течение всего времени существования данного компонента.

    Когда Angular уничтожает этот компонент, труба `async` автоматически останавливается.

    For detailed information about the `async` pipe, see the [AsyncPipe API documentation](api/common/AsyncPipe).

1.  Add a link from the `CartComponent` view to the `ShippingComponent` view.

    <code-example header="src/app/cart/cart.component.html" path="getting-started/src/app/cart/cart.component.2.html"></code-example>

1.  Click the **Checkout** button to see the updated cart.

    Remember that changing the application causes the preview to refresh, which empties the cart.

    <div class="lightbox">

    <img alt="Cart with link to shipping prices" src="generated/images/guide/start/cart-empty-with-shipping-prices.png">

    </div>

    Click on the link to navigate to the shipping prices.

    <div class="lightbox">

    <img alt="Display shipping prices" src="generated/images/guide/start/shipping-prices.png">

    </div>

## Что дальше

Теперь у вас есть приложение магазина с каталогом товаров, корзиной и возможностью поиска цен на доставку.

Чтобы продолжить знакомство с Angular:

-   Перейдите к разделу [Формы для пользовательского ввода](start/start-forms 'Forms for User Input'), чтобы завершить приложение, добавив представление корзины и форму оформления заказа.

-   Перейдите к [Deployment](start/start-deployment 'Развертывание'), чтобы перейти к локальной разработке или развернуть приложение на Firebase или собственном сервере.

:date: 28.02.2022
