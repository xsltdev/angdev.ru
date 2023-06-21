# Взаимодействие компонентов

<a id="top"></a>

Эта поваренная книга содержит рецепты для распространенных сценариев взаимодействия компонентов, в которых два или более компонентов обмениваются информацией.

<a id="toc"></a>

<!-- # Contents

*   [Pass data from parent to child with input binding](guide/component-interaction#parent-to-child)
*   [Intercept input property changes with a setter](guide/component-interaction#parent-to-child-setter)
*   [Intercept input property changes with `ngOnChanges()`](guide/component-interaction#parent-to-child-on-changes)
*   [Parent calls an `@ViewChild()`](guide/component-interaction#parent-to-view-child)
*   [Parent and children communicate via a service](guide/component-interaction#bidirectional-service)
-->

**Смотрите <live-example name="component-interaction"></live-example>**.

<a id="parent-to-child"></a>

## Передача данных от родителя к ребенку с помощью привязки ввода

`HeroChildComponent` имеет два **_input свойства_**, обычно украшенные декоратором [@Input()](guide/inputs-outputs#input).

<code-example header="component-interaction/src/app/hero-child.component.ts" path="component-interaction/src/app/hero-child.component.ts"></code-example>.

Второй `@Input` псевдонизирует имя свойства дочернего компонента `masterName` как `'master'`.

Родительский компонент `HeroParentComponent` вставляет дочерний компонент `HeroChildComponent` внутрь повторителя `*ngFor`, связывая его строковое свойство `master` с псевдонимом `master` дочернего компонента, а экземпляр `hero` каждой итерации - со свойством `hero` дочернего компонента.

<code-example header="component-interaction/src/app/hero-parent.component.ts" path="component-interaction/src/app/hero-parent.component.ts"></code-example>.

Запущенное приложение отображает трех героев:

<div class="lightbox">

<img alt="Parent-to-child" src="generated/images/guide/component-interaction/parent-to-child.png">

</div>

### Протестируйте его на передачу данных от родителя к ребенку с привязкой к входу

E2E проверка того, что все дочерние элементы были созданы и отображены, как ожидалось:

<code-example header="component-interaction/e2e/src/app.e2e-spec.ts" path="component-interaction/e2e/src/app.e2e-spec.ts" region="parent-to-child"></code-example>

[Вернуться к началу](guide/component-interaction#top)

<a id="parent-to-child-setter"></a>

## Перехват изменений входного свойства с помощью сеттера

Используйте сеттер входного свойства, чтобы перехватить значение от родителя и действовать в соответствии с ним.

Сеттер входного свойства `name` в дочернем `NameChildComponent` удаляет пробелы из имени и заменяет пустое значение текстом по умолчанию.

<code-example header="component-interaction/src/app/name-child.component.ts" path="component-interaction/src/app/name-child.component.ts"></code-example>

Вот `NameParentComponent`, демонстрирующий варианты имен, включая имя со всеми пробелами:

<code-example header="component-interaction/src/app/name-parent.component.ts" path="component-interaction/src/app/name-parent.component.ts"></code-example>

<div class="lightbox">

<img alt="Parent-to-child-setter" src="generated/images/guide/component-interaction/setter.png">

</div>

### Тест на перехват изменений входного свойства с помощью сеттера

E2E тесты сеттера входного свойства с пустыми и непустыми именами:

<code-example header="component-interaction/e2e/src/app.e2e-spec.ts" path="component-interaction/e2e/src/app.e2e-spec.ts" region="parent-to-child-setter"></code-example>

[Вернуться к началу](guide/component-interaction#top)

<a id="parent-to-child-on-changes"></a>

## Перехват изменений свойств ввода с помощью `ngOnChanges()`.

Обнаруживайте изменения значений входных свойств и действуйте в соответствии с ними с помощью метода `ngOnChanges()` интерфейса хука жизненного цикла `OnChanges`.

<div class="alert is-helpful">

Вы можете предпочесть этот подход к установщику свойств при наблюдении за несколькими взаимодействующими свойствами ввода.

Узнайте о `ngOnChanges()` в главе [Lifecycle Hooks](guide/lifecycle-hooks).

</div>

Этот `VersionChildComponent` обнаруживает изменения входных свойств `major` и `minor` и составляет сообщение журнала, сообщающее об этих изменениях:

<code-example header="component-interaction/src/app/version-child.component.ts" path="component-interaction/src/app/version-child.component.ts"></code-example>.

Компонент `VersionParentComponent` предоставляет значения `minor` и `major` и привязывает кнопки к методам, которые их изменяют.

<code-example header="component-interaction/src/app/version-parent.component.ts" path="component-interaction/src/app/version-parent.component.ts"></code-example>

Вот результат последовательности нажатия кнопки:

<div class="lightbox">

<img alt="Parent-to-child-onchanges" src="generated/images/guide/component-interaction/parent-to-child-on-changes.gif">

</div>

### Протестируйте его на перехват изменений свойств ввода с помощью `ngOnChanges()`.

Проверьте, что **_обои_** входные свойства установлены изначально и что нажатие на кнопку вызывает ожидаемые вызовы и значения `ngOnChanges`:

<code-example header="component-interaction/e2e/src/app.e2e-spec.ts" path="component-interaction/e2e/src/app.e2e-spec.ts" region="parent-to-child-onchanges"></code-example>

[Назад к началу](guide/component-interaction#top)

<a id="child-to-parent"></a>

## Родитель слушает событие ребенка

Дочерний компонент раскрывает свойство `EventEmitter`, с помощью которого он `издает` события, когда что-то происходит. Родитель привязывается к этому свойству событий и реагирует на эти события.

Свойство дочернего компонента `EventEmitter` является **_выводным свойством_**, обычно украшенным декоратором [@Output()](guide/inputs-outputs#output), как показано в этом `VoterComponent`:

<code-example header="component-interaction/src/app/voter.component.ts" path="component-interaction/src/app/voter.component.ts"></code-example>.

Нажатие на кнопку вызывает испускание `true` или `false`, булевой _payload_.

Родительский `VoteTakerComponent` связывает обработчик события `onVoted()`, который реагирует на дочернее событие полезной нагрузки `$event` и обновляет счетчик.

<code-example header="component-interaction/src/app/votetaker.component.ts" path="component-interaction/src/app/votetaker.component.ts"></code-example>.

Фреймворк передает аргумент события &mdash;представленный `$event`&mdash; в метод обработчика, и метод обрабатывает его:

<div class="lightbox">

<img alt="Child-to-parent" src="generated/images/guide/component-interaction/child-to-parent.gif">

</div>

### Проверьте, что родитель прослушивает событие ребенка.

Проверьте, что нажатие кнопок _Согласен_ и _Не согласен_ обновляет соответствующие счетчики:

<code-example header="component-interaction/e2e/src/app.e2e-spec.ts" path="component-interaction/e2e/src/app.e2e-spec.ts" region="child-to-parent"></code-example>

[Вернуться к началу](guide/component-interaction#top)

## Родитель взаимодействует с ребенком, используя _локальную переменную_.

Родительский компонент не может использовать привязку данных для чтения дочерних свойств или вызова дочерних методов. Для этого нужно создать переменную-ссылку шаблона для дочернего элемента, а затем ссылаться на эту переменную _в родительском шаблоне_, как показано в следующем примере.

<a id="countdown-timer-example"></a>

Ниже представлен дочерний `CountdownTimerComponent`, который многократно отсчитывает время до нуля и запускает ракету. Методы `start` и `stop` управляют часами, а сообщение о состоянии обратного отсчета отображается в собственном шаблоне.

<code-example header="component-interaction/src/app/countdown-timer.component.ts" path="component-interaction/src/app/countdown-timer.component.ts"></code-example>.

Родительский компонент `CountdownLocalVarParentComponent`, в котором размещается компонент таймера, выглядит следующим образом:

<code-example header="component-interaction/src/app/countdown-parent.component.ts" path="component-interaction/src/app/countdown-parent.component.ts" region="lv"></code-example>.

Родительский компонент не может привязать данные к методам `start` и `stop` дочернего компонента, а также к его свойству `seconds`.

Поместите локальную переменную `#timer` на тег `<app-countdown-timer>`, представляющий дочерний компонент. Это даст вам ссылку на дочерний компонент и возможность доступа к _любым его свойствам или методам_ из родительского шаблона.

В этом примере родительские кнопки подключаются к дочерним `start` и `stop`, а для отображения дочернего свойства `seconds` используется интерполяция.

Здесь родитель и ребенок работают вместе.

<div class="lightbox">

<img alt="countdown timer" src="generated/images/guide/component-interaction/countdown-timer-anim.gif">

</div>

<a id="countdown-tests"></a>

### Проверьте, что родитель взаимодействует с ребенком с помощью _локальной переменной_.

Проверьте, что секунды, отображаемые в шаблоне родителя, совпадают с секундами, отображаемыми в сообщении о статусе ребенка. Проверьте также, что нажатие кнопки _Stop_ приостанавливает таймер обратного отсчета:

<code-example header="component-interaction/e2e/src/app.e2e-spec.ts" path="component-interaction/e2e/src/app.e2e-spec.ts" region="countdown-timer-tests"></code-example>

[Назад к началу](guide/component-interaction#top)

<a id="parent-to-view-child"></a>

## Родитель вызывает `@ViewChild()`.

Подход _локальной переменной_ является простым. Но он ограничен, поскольку связь между родителями и детьми должна осуществляться исключительно в родительском шаблоне.

Родительский компонент _сам по себе_ не имеет доступа к дочернему.

Вы не можете использовать технику _локальной переменной_, если _класс_ родительского компонента зависит от _класса_ дочернего компонента. Отношения "родитель-ребенок" компонентов не устанавливаются внутри соответствующего _класса_ каждого компонента с помощью техники _локальной переменной_.

Поскольку экземпляры _класса_ не связаны друг с другом, родительский _класс_ не может получить доступ к свойствам и методам дочернего _класса_.

Когда родительский компонент _класса_ требует такого доступа, **_вставьте_** дочерний компонент в родительский как _ViewChild_.

Следующий пример иллюстрирует эту технику на примере того же [Countdown Timer](guide/component-interaction#countdown-timer-example). Ни его внешний вид, ни поведение не меняются.

Дочерний [CountdownTimerComponent](guide/component-interaction#countdown-timer-example) также не меняется.

<div class="alert is-helpful">

Переход от _локальной переменной_ к технике _ViewChild_ осуществляется исключительно в целях демонстрации.

</div>

Здесь находится родитель, `CountdownViewChildParentComponent`:

<code-example header="component-interaction/src/app/countdown-parent.component.ts" path="component-interaction/src/app/countdown-parent.component.ts" region="vc"></code-example>.

Потребуется немного больше работы, чтобы вписать дочернее представление в класс _класса_ родительского компонента.

Сначала нужно импортировать ссылки на декоратор `ViewChild` и хук жизненного цикла `AfterViewInit`.

Затем внедрите дочерний `CountdownTimerComponent` в частное свойство `timerComponent`, используя декоратор свойства `@ViewChild`.

Локальная переменная `#timer` исчезнет из метаданных компонента. Вместо этого привяжите кнопки к собственным методам родительского компонента `start` и `stop` и представьте тикающие секунды в интерполяции вокруг метода родительского компонента `seconds`.

Эти методы обращаются непосредственно к инжектированному компоненту таймера.

Крючок жизненного цикла `ngAfterViewInit()` является важным моментом. Компонент таймера становится доступным только после того, как Angular отобразит родительское представление.

Поэтому первоначально он отображает `0` секунд.

Затем Angular вызывает хук жизненного цикла `ngAfterViewInit`, и в это время уже _слишком поздно_ обновлять отображение секунд обратного отсчета в родительском представлении. Правило однонаправленного потока данных Angular не позволяет обновить родительское представление в том же цикле.

Приложение должно _выждать один оборот_, прежде чем оно сможет отобразить секунды.

Используйте `setTimeout()` для ожидания одного такта, а затем пересмотрите метод `seconds()` так, чтобы он принимал будущие значения от компонента таймера.

### Протестируйте его на вызов родительского компонента `@ViewChild()`.

Используйте [те же тесты таймера обратного отсчета](guide/component-interaction#countdown-tests), что и раньше.

[Back to top](guide/component-interaction#top)

<a id="bidirectional-service"></a>

## Родительский и дочерний компоненты общаются с помощью сервиса

Родительский компонент и его дочерние компоненты совместно используют сервис, интерфейс которого обеспечивает двунаправленную связь _в пределах семейства_.

Областью действия экземпляра сервиса является родительский компонент и его дочерние компоненты. Компоненты вне этого поддерева компонентов не имеют доступа к сервису или их коммуникациям.

Этот `MissionService` соединяет `MissionControlComponent` с несколькими дочерними `AstronautComponent`.

<code-example header="component-interaction/src/app/mission.service.ts" path="component-interaction/src/app/mission.service.ts"></code-example>.

Компонент `MissionControlComponent` предоставляет экземпляр сервиса, который он разделяет со своими дочерними компонентами\ (через массив метаданных `providers`)\ и внедряет этот экземпляр в себя через свой конструктор:

<code-example header="component-interaction/src/app/missioncontrol.component.ts" path="component-interaction/src/app/missioncontrol.component.ts"></code-example>.

Компонент `AstronautComponent` также инжектирует сервис в своем конструкторе. Каждый `AstronautComponent` является дочерним компонентом `MissionControlComponent` и поэтому получает экземпляр службы своего родителя:

<code-example header="component-interaction/src/app/astronaut.component.ts" path="component-interaction/src/app/astronaut.component.ts"></code-example>

<div class="alert is-helpful">

Обратите внимание, что в этом примере фиксируется `subscription` и `unsubscribe()` при уничтожении `AstronautComponent`. Это шаг защиты от утечки памяти.
В этом приложении нет фактического риска, потому что время жизни `AstronautComponent` равно времени жизни самого приложения.

Это _не всегда_ будет верно в более сложном приложении.

Вы не добавляете эту защиту к `MissionControlComponent`, потому что, как родитель, он контролирует время жизни `MissionService`.

</div>

Журнал _History_ демонстрирует, что сообщения перемещаются в обоих направлениях между родительским `MissionControlComponent` и дочерними `AstronautComponent`, чему способствует служба:

<div class="lightbox">

<img alt="bidirectional-service" src="generated/images/guide/component-interaction/bidirectional-service.gif">

</div>

### Тестирование взаимодействия родительского и дочернего компонентов с помощью службы

Тестирует нажатие на кнопки как родительского `MissionControlComponent`, так и дочернего `AstronautComponent` и проверяет, что история соответствует ожиданиям:

<code-example header="component-interaction/e2e/src/app.e2e-spec.ts" path="component-interaction/e2e/src/app.e2e-spec.ts" region="bidirectional-service"></code-example>

[Назад к началу](guide/component-interaction#top)

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
