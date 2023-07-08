# Уведомления работников службы

:date: 28.02.2022

**Push-уведомления** - убедительный способ привлечь пользователей. Благодаря возможностям рабочих служб, уведомления могут быть доставлены на устройство, даже когда ваше приложение не находится в фокусе.

Рабочий сервис Angular позволяет отображать push-уведомления и обрабатывать события нажатия на уведомление.

!!!note ""

    При использовании Angular service worker взаимодействие с push-уведомлениями осуществляется с помощью службы `SwPush`. Более подробную информацию о соответствующих API браузера можно найти в разделах [Push API](https://developer.mozilla.org/docs/Web/API/Push_API) и [Using the Notifications API](https://developer.mozilla.org/docs/Web/API/Notifications_API/Using_the_Notifications_API).

## Предварительные условия

Мы рекомендуем вам иметь базовое представление о следующем:

-   [Начало работы с Service Workers](service-worker-getting-started.md)

## Полезная нагрузка уведомления

Вызовите push-уведомления, отправив сообщение с правильной полезной нагрузкой. Смотрите `SwPush` для руководства.

!!!note ""

    В Chrome можно тестировать push-уведомления без бэкенда. Откройте Devtools -&gt; Application -&gt; Service Workers и используйте вход `Push` для отправки полезной нагрузки JSON-уведомления.

## Обработка щелчков уведомлений

Поведение по умолчанию для события `notificationclick` заключается в закрытии уведомления и уведомлении `SwPush.notificationClicks`.

Вы можете указать дополнительную операцию, которая будет выполняться при `notificationclick`, добавив свойство `onActionClick` к объекту `data` и предоставив запись `default`. Это особенно полезно, когда при нажатии на уведомление нет открытых клиентов.

```json
{
    "notification": {
        "title": "New Notification!",
        "data": {
            "onActionClick": {
                "default": {
                    "operation": "openWindow",
                    "url": "foo"
                }
            }
        }
    }
}
```

### Операции

Angular service worker поддерживает следующие операции:

| Операции                    | Подробности                                                                                                                                            |
| :-------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `openWindow`                | Открывает новую вкладку по указанному URL.                                                                                                             |
| `focusLastFocusedOrOpen`    | Фокусирует последнего сфокусированного клиента. Если клиент не открыт, то открывает новую вкладку по указанному URL.                                   |
| `navigateLastFocusedOrOpen` | Фокусирует последнего сфокусированного клиента и переводит его на указанный URL. Если клиент не открыт, то открывается новая вкладка на указанном URL. |
| `sendRequest`               | Отправляет простой GET-запрос на указанный URL.                                                                                                        |

!!!warning ""

    URL разрешаются относительно области регистрации работника сервиса.

    Если элемент `onActionClick` не определяет `url`, то используется область регистрации работника сервиса.

### Действия

Действия позволяют настроить взаимодействие пользователя с уведомлением.

Используя свойство `actions`, вы можете определить набор доступных действий. Каждое действие представлено в виде кнопки действия, которую пользователь может нажать, чтобы взаимодействовать с уведомлением.

Кроме того, используя свойство `onActionClick` объекта `data`, вы можете связать каждое действие с операцией, которая будет выполнена при нажатии на соответствующую кнопку действия:

```json
{
  "notification": {
    "title": "New Notification!",
    "actions": [
      {"action": "foo", "title": "Open new tab"},
      {"action": "bar", "title": "Focus last"},
      {"action": "baz", "title": "Navigate last"},
      {"action": "qux", "title": "Send request in the background"}
      {"action": "other", "title": "Just notify existing clients"}
    ],
    "data": {
      "onActionClick": {
        "default": {"operation": "openWindow"},
        "foo": {"operation": "openWindow", "url": "/absolute/path"},
        "bar": {"operation": "focusLastFocusedOrOpen", "url": "relative/path"},
        "baz": {"operation": "navigateLastFocusedOrOpen", "url": "https://other.domain.com/"},
        "qux": {"operation": "sendRequest", "url": "https://yet.another.domain.com/"}
      }
    }
  }
}
```

!!!warning ""

    Если у действия нет соответствующей записи `onActionClick`, то уведомление закрывается, а на существующих клиентов приходит уведомление `SwPush.notificationClicks`.

## Больше об Angular service workers

Возможно, вас также заинтересует следующее:

-   [Service Worker в продакшне](service-worker-devops.md)

<!-- links -->

<!-- external links -->

<!-- end links -->
