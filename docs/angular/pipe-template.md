# Использование пайпов в шаблоне

:date: 7.04.2022

Для применения пайпа используйте оператор пайпа (`|`) в выражении шаблона, как показано в следующем примере кода, вместе с _именем_ пайпа, которое является `date` для встроенного [`DatePipe`](https://angular.io/api/common/DatePipe).

На вкладках в примере показано следующее:

-   `app.component.html` использует `date` в отдельном шаблоне для отображения дня рождения.
-   `hero-birthday1.component.ts` использует тот же пайп как часть встроенного шаблона в компоненте, который также устанавливает значение дня рождения.

=== "src/app/app.component.html"

    ```html
    <p>The hero's birthday is {{ birthday | date }}</p>
    ```

=== "src/app/hero-birthday1.component.ts"

    ```ts
    import { Component } from '@angular/core';

    @Component({
    	selector: 'app-hero-birthday',
    	template:
    		"<p>The hero's birthday is {{ birthday | date }}</p>",
    })
    export class HeroBirthdayComponent {
    	// April 15, 1988 -- since month parameter is zero-based
    	birthday = new Date(1988, 3, 15);
    }
    ```

Значение `birthday` компонента передается через оператор pipe, `|` в функцию [`date`](https://angular.io/api/common/DatePipe).
