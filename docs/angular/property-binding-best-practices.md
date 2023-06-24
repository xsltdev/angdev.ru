# Лучшие практики связывания свойств

Следуя нескольким рекомендациям, вы можете использовать связывание свойств таким образом, чтобы уменьшить количество ошибок и сохранить читабельность кода.

<div class="alert is-helpful">

Смотрите <live-example name="property-binding"></live-example> для рабочего примера, содержащего фрагменты кода из этого руководства.

</div>

## Избегайте побочных эффектов

Оценка шаблонного выражения не должна иметь видимых побочных эффектов. Используйте синтаксис шаблонных выражений, чтобы избежать побочных эффектов.

В целом, правильный синтаксис не позволяет присваивать значение чему-либо в выражении привязки свойств.

Синтаксис также не позволяет использовать операторы инкремента и декремента.

### Пример возникновения побочных эффектов

Если у вас есть выражение, которое изменяет значение чего-то другого, к чему вы привязываете свойство, то это изменение значения будет побочным эффектом. Angular может отобразить измененное значение, а может и не отобразить.

Если Angular обнаружит изменение, он выдаст ошибку.

В качестве лучшей практики используйте только те свойства и методы, которые возвращают значения.

## Возвращайте правильный тип

Выражение шаблона должно возвращать значение того типа, которое ожидает целевое свойство. Например, return:

-   a `строка`, если целевое свойство ожидает строку

-   `number`, если ожидается число

-   `object`, если ожидается объект.

### Передача строки

В следующем примере свойство `childItem` компонента `ItemDetailComponent` ожидает строку.

<code-example header="src/app/app.component.html" path="property-binding/src/app/app.component.html" region="model-property-binding"></code-example>

Подтвердите это ожидание, посмотрев в `ItemDetailComponent`, где тип `@Input()` является `string`:

<code-example header="src/app/item-detail/item-detail.component.ts (установка типа @Input())" path="property-binding/src/app/item-detail/item-detail.component.ts" region="input-type"></code-example>.

`parentItem` в `AppComponent` является строкой, что означает, что выражение `parentItem` в `[childItem]="parentItem"`, оценивается как строка.

<code-example header="src/app/app.component.ts" path="property-binding/src/app/app.component.ts" region="parent-data-type"></code-example>.

Если бы `parentItem` был каким-то другим типом, вам нужно было бы указать `childItem` `@Input()` как этот тип.

### Передача объекта

В этом примере `ItemListComponent` является дочерним компонентом `AppComponent` и свойство `items` ожидает массив объектов.

<code-example header="src/app/app.component.html" path="property-binding/src/app/app.component.html" region="pass-object"></code-example>

В `ItemListComponent` `@Input()`, `items`, имеет тип `Item[]`.

<code-example header="src/app/item-list.component.ts" path="property-binding/src/app/item-list/item-list.component.ts" region="item-input"></code-example>.

Обратите внимание, что `Item` является объектом и имеет два свойства, `id` и `name`.

<code-example header="src/app/item.ts" path="property-binding/src/app/item.ts" region="item-class"></code-example>.

В `app.component.ts`, `currentItems` - это массив объектов в той же форме, что и объект `Item` в `items.ts`, с `id` и `name`.

<code-example header="src/app.component.ts" path="property-binding/src/app/app.component.ts" region="pass-object"></code-example>.

Предоставляя объект в той же форме, вы удовлетворяете ожиданиям `items`, когда Angular оценивает выражение `currentItems`.

<!-- links -->

<!-- external links -->

<!-- end links -->

:дата: 28.02.2022
