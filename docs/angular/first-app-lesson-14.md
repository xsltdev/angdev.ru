---
description: Этот урок демонстрирует, как интегрировать HTTP и API в ваше приложение
---

# Урок 14: Добавьте HTTP-коммуникацию в ваше приложение

Этот урок демонстрирует, как интегрировать HTTP и API в ваше приложение.

До этого момента ваше приложение считывало данные из статического массива в сервисе Angular. Следующим шагом будет использование сервера JSON, с которым ваше приложение будет взаимодействовать по HTTP. HTTP-запрос будет имитировать работу с данными с сервера.

**Затраты времени:** ожидайте, что на выполнение этого урока вы потратите около 20 минут.

## Перед началом

Этот урок начинается с кода из предыдущего урока, поэтому вы можете:

-   Использовать код, созданный в Уроке 13, в своей интегрированной среде разработки (IDE).

-   Начните с примера кода из предыдущего урока. Выберите код из Урока 13, где вы можете:

    -   Использовать [живой пример](https://angular.io/generated/live-examples/first-app-lesson-13/stackblitz.html) в StackBlitz, где интерфейс StackBlitz является вашей IDE.

    -   Использовать [download пример](https://angular.io/generated/zips/first-app-lesson-13/first-app-lesson-13.zip) и открыть его в вашей IDE.

Если вы не просмотрели введение, посетите учебник [Введение в Angular](first-app.md), чтобы убедиться, что у вас есть все необходимое для завершения этого урока.

## После завершения

-   Ваше приложение будет использовать данные с сервера JSON.

## Шаги урока

Выполните эти шаги в терминале на вашем локальном компьютере.

### Шаг 1 - Настройка сервера JSON

JSON Server - это инструмент с открытым исходным кодом, используемый для создания имитационных REST API. Вы будете использовать его для обслуживания данных о местоположении жилья, которые в настоящее время хранятся в службе жилья.

1.  Установите `json-server` из npm с помощью следующей команды.

    ```shell
    npm install -g json-server
    ```

2.  В корневом каталоге проекта создайте файл `db.json`. В нем будут храниться данные для `json-server`.

3.  Откройте файл `db.json` и скопируйте в него следующий код

    ```json
    {
        "locations": [
            {
                "id": 0,
                "name": "Acme Fresh Start Housing",
                "city": "Chicago",
                "state": "IL",
                "photo": "/assets/bernard-hermant-CLKGGwIBTaY-unsplash.jpg",
                "availableUnits": 4,
                "wifi": true,
                "laundry": true
            },
            {
                "id": 1,
                "name": "A113 Transitional Housing",
                "city": "Santa Monica",
                "state": "CA",
                "photo": "/assets/brandon-griggs-wR11KBaB86U-unsplash.jpg",
                "availableUnits": 0,
                "wifi": false,
                "laundry": true
            },
            {
                "id": 2,
                "name": "Warm Beds Housing Support",
                "city": "Juneau",
                "state": "AK",
                "photo": "/assets/i-do-nothing-but-love-lAyXdl1-Wmc-unsplash.jpg",
                "availableUnits": 1,
                "wifi": false,
                "laundry": false
            },
            {
                "id": 3,
                "name": "Homesteady Housing",
                "city": "Chicago",
                "state": "IL",
                "photo": "/assets/ian-macdonald-W8z6aiwfi1E-unsplash.jpg",
                "availableUnits": 1,
                "wifi": true,
                "laundry": false
            },
            {
                "id": 4,
                "name": "Happy Homes Group",
                "city": "Gary",
                "state": "IN",
                "photo": "/assets/krzysztof-hepner-978RAXoXnH4-unsplash.jpg",
                "availableUnits": 1,
                "wifi": true,
                "laundry": false
            },
            {
                "id": 5,
                "name": "Hopeful Apartment Group",
                "city": "Oakland",
                "state": "CA",
                "photo": "/assets/r-architecture-JvQ0Q5IkeMM-unsplash.jpg",
                "availableUnits": 2,
                "wifi": true,
                "laundry": true
            },
            {
                "id": 6,
                "name": "Seriously Safe Towns",
                "city": "Oakland",
                "state": "CA",
                "photo": "/assets/phil-hearing-IYfp2Ixe9nM-unsplash.jpg",
                "availableUnits": 5,
                "wifi": true,
                "laundry": true
            },
            {
                "id": 7,
                "name": "Hopeful Housing Solutions",
                "city": "Oakland",
                "state": "CA",
                "photo": "/assets/r-architecture-GGupkreKwxA-unsplash.jpg",
                "availableUnits": 2,
                "wifi": true,
                "laundry": true
            },
            {
                "id": 8,
                "name": "Seriously Safe Towns",
                "city": "Oakland",
                "state": "CA",
                "photo": "/assets/saru-robert-9rP3mxf8qWI-unsplash.jpg",
                "availableUnits": 10,
                "wifi": false,
                "laundry": false
            },
            {
                "id": 9,
                "name": "Capital Safe Towns",
                "city": "Portland",
                "state": "OR",
                "photo": "/assets/webaliser-_TPTXZd9mOo-unsplash.jpg",
                "availableUnits": 6,
                "wifi": true,
                "laundry": true
            }
        ]
    }
    ```

4.  Сохраните этот файл.

5.  Пришло время протестировать конфигурацию. Из командной строки в корне проекта выполните следующие команды.

    ```shell
    json-server --watch db.json
    ```

6.  В веб-браузере перейдите по адресу `http://localhost:3000/locations` и убедитесь, что ответ включает данные, хранящиеся в файле `db.json`.

Если у вас возникли проблемы с конфигурацией, вы можете найти более подробную информацию в [официальной документации](https://www.npmjs.com/package/json-server).

### Шаг 2 - Обновление сервиса для использования веб-сервера вместо локального массива

Источник данных настроен, следующим шагом будет обновление веб-приложения для подключения к нему и использования данных.

1.  В `src/app/housing.service.ts` внесите следующие изменения:

    1.  Обновите код, чтобы удалить свойство `housingLocationList` и массив, содержащий данные.

    2.  Добавьте строковое свойство с именем и установите значение `'http://localhost:3000/locations'`.

        ```js
        url = 'http://localhost:3000/locations';
        ```

        Этот код приведет к ошибкам в остальной части файла, поскольку он зависит от свойства `housingLocationList`. Далее мы обновим методы сервиса.

    3.  Обновите функцию `getAllHousingLocations`, чтобы она выполняла вызов веб-сервера, который вы настроили.

        ```ts
        async getAllHousingLocations(): Promise<HousingLocation[]> {
        	const data = await fetch(this.url);
        	return await data.json() ?? [];
        }
        ```

        Теперь код использует асинхронный код для выполнения `get` запроса через `HTTP`. Обратите внимание, что для этого примера в коде используется fetch. Для более продвинутых случаев использования рассмотрим использование `HttpClient`, предоставляемого Angular.

    4.  Обновите функцию `getHousingLocationsById`, чтобы сделать вызов к веб-серверу, который вы настроили.

        ```ts
        async getHousingLocationById(id: number): Promise<HousingLocation | undefined> {
        	const data = await fetch(`${this.url}/${id}`);
        	return await data.json() ?? {};
        }
        ```

    5.  Когда все обновления будут завершены, ваш обновленный сервис будет соответствовать следующему коду.

        ```ts
        import { Injectable } from '@angular/core';
        import { HousingLocation } from './housinglocation';

        @Injectable({
            providedIn: 'root',
        })
        export class HousingService {
            url = 'http://localhost:3000/locations';

            async getAllHousingLocations(): Promise<
                HousingLocation[]
            > {
                const data = await fetch(this.url);
                return (await data.json()) ?? [];
            }

            async getHousingLocationById(
                id: number
            ): Promise<HousingLocation | undefined> {
                const data = await fetch(
                    `${this.url}/${id}`
                );
                return (await data.json()) ?? {};
            }

            submitApplication(
                firstName: string,
                lastName: string,
                email: string
            ) {
                console.log(firstName, lastName, email);
            }
        }
        ```

### Шаг 3 - Обновление компонентов для использования асинхронных вызовов службы жилья

Сервер теперь читает данные из запроса `HTTP`, но компоненты, которые полагаются на службу, теперь имеют ошибки, потому что они были запрограммированы на использование синхронной версии службы.

1.  В `src/app/home/home.component.ts` обновите конструктор, чтобы использовать новую асинхронную версию метода `getAllHousingLocations`.

    ```ts
    constructor() {
    	this.housingService.getAllHousingLocations().then((housingLocationList: HousingLocation[]) => {
    		this.housingLocationList = housingLocationList;
    		this.filteredLocationList = housingLocationList;
    	});
    }
    ```

2.  В `src/app/details/details.component.ts` обновите конструктор, чтобы использовать новую асинхронную версию метода `getHousingLocationById`.

    ```ts
    constructor() {
    	const housingLocationId = parseInt(this.route.snapshot.params['id'], 10);
    	this.housingService.getHousingLocationById(housingLocationId).then(housingLocation => {
    		this.housingLocation = housingLocation;
    	});
    }
    ```

3.  Сохраните свой код.

4.  Откройте приложение в браузере и убедитесь, что оно работает без ошибок.

## Обзор урока

В этом уроке вы обновили свое приложение, чтобы:

-   использовать локальный веб-сервер (`json-server`)

-   использовать асинхронные методы сервиса для получения данных.

Поздравляем! Вы успешно завершили этот урок и готовы продолжить свое путешествие по созданию еще более сложных приложений Angular Apps. Если вы хотите узнать больше, пожалуйста, рассмотрите другие [учебники](./first-app.md) и [руководства](developer-guide-overview.md) по Angular для разработчиков.

## Ссылки

-   [Lesson 14: Add HTTP communication to your app](https://angular.io/tutorial/first-app/first-app-lesson-14)
