# Использование трубы в шаблоне

Для применения трубы используйте оператор трубы (`|`) в выражении шаблона, как показано в следующем примере кода, вместе с _именем_ трубы, которое является `date` для встроенного [`DatePipe`](api/common/DatePipe).

На вкладках в примере показано следующее:

-   `app.component.html` использует `date` в отдельном шаблоне для отображения дня рождения.
-   `hero-birthday1.component.ts` использует ту же трубу как часть встроенного шаблона в компоненте, который также устанавливает значение дня рождения.

<code-tabs>
    <code-pane header="src/app/app.component.html" region="hero-birthday-template" path="pipes/src/app/app.component.html"></code-pane>
    <code-pane header="src/app/hero-birthday1.component.ts" path="pipes/src/app/hero-birthday1.component.ts"></code-pane>
</code-tabs>

Значение `birthday` компонента передается через оператор pipe, `|` в функцию [`date`](api/common/DatePipe).

@reviewed 2022-04-07
