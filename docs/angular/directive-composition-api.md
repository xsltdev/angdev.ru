# API композиции директив

Директивы Angular - это отличный способ инкапсулировать многократно используемое поведение: директивы могут применять к элементу атрибуты, CSS-классы и слушатели событий.

API _directive composition API_ позволяет применять директивы к главному элементу компонента из _внутри_ TypeScript-класса компонента.

## Добавление директив к компоненту

Вы применяете директивы к компоненту, добавляя свойство `hostDirectives` к декоратору компонента. Мы называем такие директивы _хост-директивами_.

В этом примере мы применяем директиву `MenuBehavior` к хост-элементу `AdminMenu`. Это работает аналогично применению `MenuBehavior` к элементу `<admin-menu>` в шаблоне.

```typescript
@Component({
    selector: 'admin-menu',
    template: 'admin-menu.html',
    hostDirectives: [MenuBehavior],
})
export class AdminMenu {}
```

Когда фреймворк рендерит компонент, Angular также создает экземпляр каждой директивы host. Привязка директив к хосту применяется к хост-элементу компонента. По умолчанию входы и выходы директив хоста
и выходы не отображаются как часть публичного API компонента. См.

[Включение входов и выходов](#including-inputs-and-outputs) ниже для получения дополнительной информации.

**Angular применяет директивы хоста статически во время компиляции.** Вы не можете динамически добавлять директивы во время выполнения.

**Директивы, используемые в `hostDirectives`, должны быть `standalone: true`.**.

**Angular игнорирует `selector` директив, применяемых в свойстве `hostDirectives`.**.

## Включение входов и выходов

Когда вы применяете `hostDirectives` к вашему компоненту, входы и выходы из директив хоста по умолчанию не включаются в API вашего компонента. Вы можете явно включить входы и выходы

в API вашего компонента, расширив запись в `hostDirectives`:

```typescript
@Component({
    selector: 'admin-menu',
    template: 'admin-menu.html',
    hostDirectives: [
        {
            directive: MenuBehavior,
            inputs: ['menuId'],
            outputs: ['menuClosed'],
        },
    ],
})
export class AdminMenu {}
```

Явно указывая входы и выходы, потребители компонента с `hostDirective` могут связать их в шаблоне:

```html
<admin-menu
    menuId="top-menu"
    (menuClosed)="logMenuClosed()"
></admin-menu>
```

Кроме того, вы можете псевдонизировать входы и выходы из `hostDirective`, чтобы настроить API вашего компонента:

```typescript
@Component({
    selector: 'admin-menu',
    template: 'admin-menu.html',
    hostDirectives: [
        {
            directive: MenuBehavior,
            inputs: ['menuId: id'],
            outputs: ['menuClosed: closed'],
        },
    ],
})
export class AdminMenu {}
```

```html
<admin-menu
    id="top-menu"
    (closed)="logMenuClosed()"
></admin-menu>
```

## Добавление директив к другой директиве

Вы также можете добавлять `hostDirectives` к другим директивам, в дополнение к компонентам. Это позволяет осуществлять переходное объединение нескольких поведений.

В следующем примере мы определяем две директивы, `Menu` и `Tooltip`. Затем мы объединяем поведение этих двух директив в `MenuWithTooltip`. Наконец, мы применяем `MenuWithTooltip`

к `SpecializedMenuWithTooltip`.

Когда `SpecializedMenuWithTooltip` используется в шаблоне, он создает экземпляры всех `Menu`, `Tooltip` и `MenuWithTooltip`. Привязка к хосту каждой из этих директив применяется к элементу host

элемента `SpecializedMenuWithTooltip`.

```typescript
 @Directive({...})
export class Menu { }

@Directive({...})
export class Tooltip { }

// MenuWithTooltip can compose behaviors from multiple other directives
@Directive({
  hostDirectives: [Tooltip, Menu],
})
export class MenuWithTooltip { }

// CustomWidget can apply the already-composed behaviors from MenuWithTooltip
@Directive({
  hostDirectives: [MenuWithTooltip],
})
export class SpecializedMenuWithTooltip { }
```

## Семантика директивы хоста

### Порядок выполнения директив

Директивы хоста проходят через тот же жизненный цикл, что и компоненты и директивы, используемые непосредственно в шаблоне. Однако директивы хоста всегда выполняют свой конструктор, крючки жизненного цикла и привязки _ до_ компонента или директивы, к которым они применяются.

до\_ компонента или директивы, к которым они применяются.

В следующем примере показано минимальное использование директивы host:

```typescript
@Component({
    selector: 'admin-menu',
    template: 'admin-menu.html',
    hostDirectives: [MenuBehavior],
})
export class AdminMenu {}
```

Порядок выполнения следующий:

1. инстанцируется `MenuBehavior

2. `AdminMenu` инстанцировано

3. `MenuBehavior` получает входные данные (`ngOnInit`)

4. `AdminMenu` получает входные данные (`ngOnInit`)

5. `MenuBehavior` применяет привязку к хосту

6. `AdminMenu` применяет привязки к хосту

Такой порядок действий означает, что компоненты с `hostDirectives` могут переопределять любые привязки хоста, указанные директивой хоста.

Этот порядок операций распространяется на вложенные цепочки директив хоста, как показано в следующем примере.

```typescript
 @Directive({...})
export class Tooltip { }

@Directive({
  hostDirectives: [Tooltip],
})
export class CustomTooltip { }

@Directive({
  hostDirectives: [CustomTooltip],
})
export class EvenMoreCustomTooltip { }
```

В приведенном выше примере порядок выполнения следующий:

1. Создается `Tooltip`

2. Создается `CustomTooltip`.

3. `EvenMoreCustomTooltip` инстанцирован

4. `Толтип` получает входные данные (`ngOnInit`)

5. `CustomTooltip` получает входные данные (`ngOnInit`)

6. `EvenMoreCustomTooltip` получает входные данные (`ngOnInit`)

7. `Tooltip` применяет привязку к хосту

8. `CustomTooltip` применяет привязки к хосту

9. `EvenMoreCustomTooltip` применяет привязку к хосту

### Инъекция зависимостей

Компонент или директива, в которой указаны `hostDirectives`, может инжектировать экземпляры этих директив хоста и наоборот.

При применении директив хоста к компоненту, как компонент, так и директивы хоста могут определять провайдеров.

Если компонент или директива с `hostDirectives` и эти директивы хоста предоставляют один и тот же маркер инъекции, провайдеры, определенные классом с `hostDirectives`, имеют приоритет над провайдерами, определенными директивами хоста.

определенными директивами хоста.

### Производительность

Хотя API композиции директив предлагает мощный инструмент для повторного использования общих моделей поведения, чрезмерное использование директив хоста может повлиять на использование памяти вашим приложением. Если вы создаете компоненты или

директивы, которые используют _множество_ директив хоста, вы можете непреднамеренно увеличить объем памяти, используемой вашим приложением.

приложением.

В следующем примере показан компонент, который применяет несколько директив хоста.

```typescript
@Component({
    hostDirectives: [
        DisabledState,
        RequiredState,
        ValidationState,
        ColorState,
        RippleBehavior,
    ],
})
export class CustomCheckbox {}
```

В этом примере объявлен компонент пользовательского флажка, который включает пять директив хоста. Это означает, что Angular будет создавать шесть объектов при каждом рендеринге `CustomCheckbox` - один для
компонента и по одному для каждой директивы-хоста. Для нескольких флажков на странице это не создаст никаких

существенных проблем. Однако, если на вашей странице отображаются _сотни_ флажков, например, в таблице, тогда

вы можете начать ощущать влияние дополнительных выделений объектов. Всегда проверяйте профиль

вашего приложения, чтобы определить правильный шаблон композиции для вашего случая использования.

:date: 11.12.2022
