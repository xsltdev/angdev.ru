# Использование форм для ввода данных пользователем

Это руководство основано на шаге [Управление данными](start-data.md) учебника [Начните работу с базовым приложением Angular](start.md).

В этом разделе вы узнаете, как добавить функцию оформления заказа на основе формы для сбора информации о пользователе в процессе оформления заказа.

## Определите модель формы оформления заказа

Этот шаг показывает, как определить модель формы оформления заказа в классе компонента. Модель формы определяет состояние формы.

**1.** Откройте `cart.component.ts`.

**2.** Импортируйте сервис `FormBuilder` из пакета `@angular/forms`. Этот сервис предоставляет удобные методы для генерации элементов управления.

```ts title="src/app/cart/cart.component.ts"
import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';

import { CartService } from '../cart.service';
```

**3.** Вставьте сервис `FormBuilder` в `конструктор()` компонента `CartComponent`. Этот сервис является частью модуля `ReactiveFormsModule`, который вы уже импортировали.

```ts title="src/app/cart/cart.component.ts"
export class CartComponent {
    constructor(
        private cartService: CartService,
        private formBuilder: FormBuilder
    ) {}
}
```

**4.** Чтобы собрать имя и адрес пользователя, используйте метод `FormBuilder` `group()` для установки свойства `checkoutForm` в модель формы, содержащую поля `name` и `address`.

```ts title="src/app/cart/cart.component.ts"
export class CartComponent {
    items = this.cartService.getItems();

    checkoutForm = this.formBuilder.group({
        name: '',
        address: '',
    });

    constructor(
        private cartService: CartService,
        private formBuilder: FormBuilder
    ) {}
}
```

**5.** Определите метод `onSubmit()` для обработки формы. Этот метод позволяет пользователям вводить свое имя и адрес. Кроме того, этот метод использует метод `clearCart()` службы `CartService` для сброса формы и очистки корзины. Весь класс компонента корзины выглядит следующим образом:

```ts title="src/app/cart/cart.component.ts"
import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';

import { CartService } from '../cart.service';

@Component({
    selector: 'app-cart',
    templateUrl: './cart.component.html',
    styleUrls: ['./cart.component.css'],
})
export class CartComponent {
    items = this.cartService.getItems();

    checkoutForm = this.formBuilder.group({
        name: '',
        address: '',
    });

    constructor(
        private cartService: CartService,
        private formBuilder: FormBuilder
    ) {}

    onSubmit(): void {
        // Process checkout data here
        this.items = this.cartService.clearCart();
        console.warn(
            'Your order has been submitted',
            this.checkoutForm.value
        );
        this.checkoutForm.reset();
    }
}
```

## Создание формы оформления заказа

Используйте следующие шаги, чтобы добавить форму оформления заказа в нижней части представления "Корзина".

**1.** В нижней части `cart.component.html` добавьте элемент HTML `<form>` и кнопку **Покупка**.

**2.** Используйте привязку свойства `formGroup` для привязки `checkoutForm` к HTML `<form>`.

```html title="src/app/cart/cart.component.html"
<form [formGroup]="checkoutForm">
    <button class="button" type="submit">Purchase</button>
</form>
```

**3.** В теге `form` используйте привязку события `ngSubmit` для прослушивания отправки формы и вызова метода `onSubmit()` со значением `checkoutForm`.

```html title="src/app/cart/cart.component.html"
<form
    [formGroup]="checkoutForm"
    (ngSubmit)="onSubmit()"
></form>
```

**4.** Добавьте поля `<input>` для `name` и `address`, каждое с атрибутом `formControlName`, который связывает с элементами управления формы `checkoutForm` для `name` и `address` их поля `<input>`.

Полный компонент выглядит следующим образом:

```html title="src/app/cart/cart.component.html"
<h3>Cart</h3>

<p>
    <a routerLink="/shipping">Shipping Prices</a>
</p>

<div class="cart-item" *ngFor="let item of items">
    <span>{{ item.name }} </span>
    <span>{{ item.price | currency }}</span>
</div>

<form [formGroup]="checkoutForm" (ngSubmit)="onSubmit()">
    <div>
        <label for="name"> Name </label>
        <input
            id="name"
            type="text"
            formControlName="name"
        />
    </div>

    <div>
        <label for="address"> Address </label>
        <input
            id="address"
            type="text"
            formControlName="address"
        />
    </div>

    <button class="button" type="submit">Purchase</button>
</form>
```

Положив несколько товаров в корзину, пользователи могут просмотреть свои товары, ввести свое имя и адрес и отправить покупку.

![Вид корзины с формой оформления заказа](cart-with-items-and-form.png)

Чтобы подтвердить отправку, откройте консоль и увидите объект, содержащий имя и адрес, которые вы отправили.

## Что дальше

У вас есть готовое приложение интернет-магазина с каталогом товаров, корзиной и функцией оформления заказа.

Перейдите к разделу ["Развертывание"](start-deployment.md), чтобы перейти к локальной разработке, или разверните приложение на Firebase или собственном сервере.

:date: 15.09.2021
