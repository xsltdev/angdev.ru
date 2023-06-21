# Использование форм для ввода данных пользователем

Это руководство основано на шаге [Управление данными](start/start-data 'Попробуйте: управление данными') учебника [Начните работу с базовым приложением Angular](start 'Начните работу с базовым приложением Angular').

В этом разделе вы узнаете, как добавить функцию оформления заказа на основе формы для сбора информации о пользователе в процессе оформления заказа.

## Определите модель формы оформления заказа

Этот шаг показывает, как определить модель формы оформления заказа в классе компонента. Модель формы определяет состояние формы.

1. Откройте `cart.component.ts`.

1. Импортируйте сервис `FormBuilder` из пакета `@angular/forms`.

Этот сервис предоставляет удобные методы для генерации элементов управления.

<code-example header="src/app/cart/cart.component.ts" path="getting-started/src/app/cart/cart.component.ts" region="imports"></code-example>

1. Вставьте сервис `FormBuilder` в `конструктор()` компонента `CartComponent`.

Этот сервис является частью модуля `ReactiveFormsModule`, который вы уже импортировали.

<code-example header="src/app/cart/cart.component.ts" path="getting-started/src/app/cart/cart.component.ts" region="inject-form-builder"></code-example>.

1. Чтобы собрать имя и адрес пользователя, используйте метод `FormBuilder` `group()` для установки свойства `checkoutForm` в модель формы, содержащую поля `name` и `address`.

<code-example header="src/app/cart/cart.component.ts" path="getting-started/src/app/cart/cart.component.ts" region="checkout-form-group"></code-example>.

1. Определите метод `onSubmit()` для обработки формы.

Этот метод позволяет пользователям вводить свое имя и адрес. Кроме того, этот метод использует метод `clearCart()` службы `CartService` для сброса формы и очистки корзины.

Весь класс компонента корзины выглядит следующим образом:

<code-example header="src/app/cart/cart.component.ts" path="getting-started/src/app/cart/cart.component.ts"></code-example>.

## Создание формы оформления заказа

Используйте следующие шаги, чтобы добавить форму оформления заказа в нижней части представления "Корзина".

1. В нижней части `cart.component.html` добавьте элемент HTML `<form>` и кнопку **Покупка**.

1. Используйте привязку свойства `formGroup` для привязки `checkoutForm` к HTML `<form>`.

<code-example header="src/app/cart/cart.component.html" path="getting-started/src/app/cart/cart.component.3.html" region="checkout-form"></code-example>.

1. В теге `form` используйте привязку события `ngSubmit` для прослушивания отправки формы и вызова метода `onSubmit()` со значением `checkoutForm`.

<code-example header="src/app/cart/cart.component.html (cart component template detail)" path="getting-started/src/app/cart/cart.component.html" region="checkout-form-1"></code-example>

1. Add `<input>` fields for `name` and `address`, each with a `formControlName` attribute that binds to the `checkoutForm` form controls for `name` and `address` to their `<input>` fields.

The complete component is as follows:

<code-example header="src/app/cart/cart.component.html" path="getting-started/src/app/cart/cart.component.html" region="checkout-form-2"></code-example>.

Положив несколько товаров в корзину, пользователи могут просмотреть свои товары, ввести свое имя и адрес и отправить покупку.

<div class="lightbox">   <img alt="Cart view with checkout form" src="generated/images/guide/start/cart-with-items-and-form.png">
</div>

Чтобы подтвердить отправку, откройте консоль и увидите объект, содержащий имя и адрес, которые вы отправили.

## Что дальше

У вас есть готовое приложение интернет-магазина с каталогом товаров, корзиной и функцией оформления заказа.

[Перейдите к разделу "Развертывание"](start/start-deployment 'Try it: Deployment'), чтобы перейти к локальной разработке, или разверните приложение на Firebase или собственном сервере.

:date: 15.09.2021
