# Управление маркированным текстом с пользовательскими идентификаторами

Экстрактор Angular генерирует файл с записью единицы перевода в каждом из следующих случаев.

-   Каждый атрибут `i18n` в шаблоне компонента

-   Каждая [`$localize`][aioapilocalizeinitlocalize] помеченная строка сообщения в коде компонента.

Как описано в [How meanings control text extraction and merges][aioguidei18ncommonpreparehowmeaningscontroltextextractionandmerges], Angular присваивает каждой единице перевода уникальный идентификатор.

В следующем примере отображаются единицы перевода с уникальными идентификаторами.

<code-example header="messages.fr.xlf.html" path="i18n/doc-files/messages.fr.xlf.html" region="generated-id"></code-example>.

Когда вы изменяете переводимый текст, экстрактор генерирует новый идентификатор для этой единицы перевода. В большинстве случаев изменения в исходном тексте требуют изменений и в переводе.

Поэтому использование нового идентификатора позволяет синхронизировать изменение текста с переводом.

Однако некоторые системы перевода требуют особой формы или синтаксиса для идентификатора. Чтобы удовлетворить это требование, используйте пользовательский идентификатор для маркировки текста.

Большинству разработчиков нет необходимости использовать пользовательский идентификатор.

Если вы хотите использовать уникальный синтаксис для передачи дополнительных метаданных, используйте пользовательский идентификатор.

Дополнительные метаданные могут включать библиотеку, компонент или область приложения, в которой появляется текст.

Чтобы указать пользовательский ID в атрибуте `i18n` или [`$localize`][aioapilocalizeinitlocalize] тегированной строки сообщения, используйте префикс `@@`. Следующий пример определяет пользовательский идентификатор `introductionHeader` в элементе заголовка.

<code-example header="app/app.component.html" path="i18n/doc-files/app.component.html" region="i18n-attribute-solo-id"></code-example>.

Следующий пример определяет пользовательский идентификатор `introductionHeader` для переменной.

<!--todo: replace with code example -->

<code-example format="typescript" language="typescript">

variableText1 = \$localize `:&commat;&commat;introductionHeader:Hello i18n!`;

</code-example>

Когда вы указываете пользовательский идентификатор, экстрактор генерирует единицу перевода с пользовательским идентификатором.

<code-example header="messages.fr.xlf.html" path="i18n/doc-files/messages.fr.xlf.html" region="custom-id"></code-example>.

Если вы измените текст, экстрактор не изменит идентификатор. В результате вам не придется делать дополнительный шаг для обновления перевода.

Недостатком использования пользовательских идентификаторов является то, что при изменении текста перевод может не синхронизироваться с новым измененным исходным текстом.

#### Использование пользовательского идентификатора с описанием

Используйте пользовательский идентификатор в сочетании с описанием и значением, чтобы еще больше помочь переводчику.

Следующий пример включает описание, за которым следует пользовательский идентификатор.

<code-example header="app/app.component.html" path="i18n/doc-files/app.component.html" region="i18n-attribute-id"></code-example>.

Следующий пример определяет пользовательский идентификатор `introductionHeader` и описание для переменной.

<!--todo: replace with code example -->

<code-example format="typescript" language="typescript">

variableText2 = \$localize `:Вводный заголовок для этого образца&commat;&commat;introductionHeader:Hello i18n!`;

</code-example>

В следующем примере добавляется значение.

<code-example header="app/app.component.html" path="i18n/doc-files/app.component.html" region="i18n-attribute-meaning-and-id"></code-example>.

Следующий пример определяет пользовательский идентификатор `introductionHeader` для переменной.

<!--todo: replace with code example -->

<code-example format="typescript" language="typescript">

variableText3 = \$localize `:site header|An introduction header for this sample&commat;&commat;introductionHeader:Hello i18n!`;

</code-example>

#### Определите уникальные пользовательские идентификаторы

Обязательно задавайте уникальные пользовательские идентификаторы. Если вы используете один и тот же идентификатор для двух разных текстовых элементов, инструмент извлечения извлечет только первый, а Angular использует перевод вместо обоих исходных текстовых элементов.

Например, в следующем фрагменте кода один и тот же пользовательский идентификатор `myId` определен для двух разных текстовых элементов.

<code-example header="app/app.component.html" path="i18n/doc-files/app.component.html" region="i18n-duplicate-custom-id"></code-example>.

Ниже показан перевод на французский язык.

<code-example header="src/locale/messages.fr.xlf" path="i18n/doc-files/messages.fr.xlf.html" region="i18n-duplicate-custom-id"></code-example>.

Оба элемента теперь используют один и тот же перевод \(`Bonjour`\), потому что оба были определены с одним и тем же пользовательским идентификатором.

<code-example path="i18n/doc-files/rendered-output.html"></code-example>

<!-- links -->

[aioapilocalizeinitlocalize]: api/localize/init/$localize '$localize | init - localize - API | Angular'
[aioguidei18ncommonpreparehowmeaningscontroltextextractionandmerges]: guide/i18n-common-prepare#how-meanings-control-text-extraction-and-merges 'How meanings control text extraction and merges - Prepare components for translations | Angular'

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
