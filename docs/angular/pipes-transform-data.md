# Преобразование данных с помощью параметров и цепочки пайпов

:date: 1.04.2022

Используйте дополнительные параметры для точной настройки вывода пайпа. Например, используйте [`CurrencyPipe`](https://angular.io/api/common/CurrencyPipe) с кодом страны, например EUR, в качестве параметра.

Шаблонное выражение `{{ amount | currency:'EUR' }}` преобразует `amount` в валюту в евро.

После имени пайпа (`currency`) следует двоеточие (`:`) и значение параметра (`'EUR'`).

Если пайп принимает несколько параметров, разделите значения двоеточиями. Например, `{{ amount | currency:'EUR':'Euros'}}` добавляет второй параметр, строковый литерал `'Euros'``, в выходную строку. В качестве параметра можно использовать любое допустимое выражение шаблона, например, строковый литерал или свойство компонента.

Некоторые пайпы требуют как минимум один параметр и допускают больше необязательных параметров, например [`SlicePipe`](https://angular.io/api/common/SlicePipe). Например, `{{ slice:1:5 }}` создает новый массив или строку, содержащую подмножество элементов, начиная с элемента `1` и заканчивая элементом `5`.

## Пример: Форматирование даты

Вкладки в следующем примере демонстрируют переключение между двумя различными форматами (`'shortDate'` и `'fullDate'`):

-   Шаблон `app.component.html` использует параметр формата для [`DatePipe`](https://angular.io/api/common/DatePipe) (с именем `date`), чтобы показать дату как **04/15/88**.
-   Компонент `hero-birthday2.component.ts` привязывает параметр формата пайпа к свойству `format` компонента в секции `template` и добавляет кнопку для события click, привязанную к методу `toggleFormat()` компонента.
-   Метод `toggleFormat()` компонента `hero-birthday2.component.ts` переключает свойство `format` компонента между краткой формой (`'shortDate'`) и более длинной формой (`'fullDate'`).

=== "src/app/app.component.html"

    ```html
    <p>
    	The hero's birthday is {{ birthday | date:"MM/dd/yy" }}
    </p>
    ```

=== "src/app/hero-birthday2.component.ts (template)"

    ```ts
    template: `
    <p>The hero's birthday is {{ birthday | date:format }}</p>
    <button type="button" (click)="toggleFormat()">Toggle Format</button>
    `;
    ```

=== "src/app/hero-birthday2.component.ts (class)"

    ```ts
    export class HeroBirthday2Component {
    	// April 15, 1988 -- since month parameter is zero-based
    	birthday = new Date(1988, 3, 15);
    	toggle = true; // start with true == shortDate

    	get format() {
    		return this.toggle ? 'shortDate' : 'fullDate';
    	}
    	toggleFormat() {
    		this.toggle = !this.toggle;
    	}
    }
    ```

При нажатии на кнопку **Toggle Format** формат даты меняется между **04/15/1988** и **Пятница, 15 апреля 1988**.

!!!note ""

    Параметры формата пайпа `date` см. в [DatePipe](https://angular.io/api/common/DatePipe).

## Пример: Применение двух форматов с помощью цепочки пайпов

Соедините пайпы в цепочку так, чтобы выход одного пайпа стал входом для следующего.

В следующем примере цепочка пайпов сначала применяет формат к значению даты, а затем преобразует отформатированную дату в заглавные символы. Первая вкладка шаблона `src/app/app.component.html` связывает `DatePipe` и `UpperCasePipe` для отображения даты рождения как **APR 15, 1988**.

Вторая вкладка шаблона `src/app/app.component.html` передает параметр `fullDate` в `date` перед цепочкой в `uppercase`, что выводит **FRIDAY, APRIL 15, 1988**.

=== "src/app/app.component.html (1)"

    ```html
    The chained hero's birthday is {{ birthday | date |
    uppercase}}
    ```

=== "src/app/app.component.html (2)"

    ```html
    The chained hero's birthday is {{ birthday | date:'fullDate'
    | uppercase}}
    ```
