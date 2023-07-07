# Начало работы с автономными компонентами

**Стандартные компоненты** обеспечивают упрощенный способ создания приложений Angular. Автономные компоненты, директивы и трубы призваны упростить процесс создания приложений за счет сокращения необходимости использования `NgModule`. Существующие приложения могут по желанию и постепенно переходить на новый автономный стиль без каких-либо ломающих изменений.

## Создание автономных компонентов

<iframe width="100%" height="400" src="https://www.youtube.com/embed/x5PZwb4XurU" title="YouTube video player" frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### Флаг `standalone` и компонентные `imports`

Компоненты, директивы и трубы теперь могут быть помечены как `standalone: true`. Классы Angular, помеченные как автономные, не нужно объявлять в `NgModule` (компилятор Angular сообщит об ошибке, если вы попытаетесь это сделать).

Автономные компоненты указывают свои зависимости напрямую, а не получают их через `NgModule`. Например, если `PhotoGalleryComponent` является автономным компонентом, он может напрямую импортировать другой автономный компонент `ImageGridComponent`:

```ts
@Component({
    standalone: true,
    selector: 'photo-gallery',
    imports: [ImageGridComponent],
    template: `
        ... <image-grid [images]="imageList"></image-grid>
    `,
})
export class PhotoGalleryComponent {
    // component logic
}
```

`imports` можно также использовать для ссылки на отдельные директивы и трубы. Таким образом, автономные компоненты могут быть написаны без необходимости создания `NgModule` для управления зависимостями шаблонов.

### Использование существующих NgModules в автономном компоненте

При написании автономного компонента вы можете захотеть использовать другие компоненты, директивы или трубы в шаблоне компонента. Некоторые из этих зависимостей могут быть не помечены как самостоятельные, а вместо этого объявлены и экспортированы существующим `NgModule`. В этом случае вы можете импортировать `NgModule` непосредственно в отдельный компонент:

```ts
@Component({
    standalone: true,
    selector: 'photo-gallery',
    // an existing module is imported directly into a standalone component
    imports: [MatButtonModule],
    template: `
        ...
        <button mat-button>Next Page</button>
    `,
})
export class PhotoGalleryComponent {
    // logic
}
```

Вы можете использовать автономные компоненты с существующими библиотеками на основе `NgModule` или зависимостями в вашем шаблоне. Автономные компоненты могут использовать все преимущества существующей экосистемы библиотек Angular.

## Использование автономных компонентов в приложениях на основе NgModule

Автономные компоненты также могут быть импортированы в существующие контексты на основе `NgModules`. Это позволяет существующим приложениям (которые используют `NgModules` сегодня) постепенно переходить на новый, автономный стиль компонента.

Вы можете импортировать отдельный компонент (или директиву, или трубу) точно так же, как и `NgModule` - используя `NgModule.imports`:

```ts
@NgModule({
    declarations: [AlbumComponent],
    exports: [AlbumComponent],
    imports: [PhotoGalleryComponent],
})
export class AlbumModule {}
```

## Загрузка приложения с помощью отдельного компонента

Приложение Angular может быть загружено без какого-либо `NgModule`, используя отдельный компонент в качестве корневого компонента приложения. Для этого используется API `bootstrapApplication`:

```ts
// in the main.ts file
import { bootstrapApplication } from '@angular/platform-browser';
import { PhotoAppComponent } from './app/photo.app.component';

bootstrapApplication(PhotoAppComponent);
```

### Настройка внедрения зависимостей

При загрузке приложения часто требуется настроить внедрение зависимостей Angular и предоставить значения конфигурации или сервисы для использования во всем приложении. Вы можете передать их в качестве провайдеров в `bootstrapApplication`:

```ts
bootstrapApplication(PhotoAppComponent, {
    providers: [
        {
            provide: BACKEND_URL,
            useValue:
                'https://photoapp.looknongmodules.com/api',
        },
        // ...
    ],
});
```

Автономная работа `bootstrap` основана на явной настройке списка `Provider` для инъекции зависимостей. В Angular функции с префиксом `provide` можно использовать для настройки различных систем без необходимости импортировать `NgModules`. Например, `provideRouter` используется вместо `RouterModule.forRoot` для настройки маршрутизатора:

```ts
bootstrapApplication(PhotoAppComponent, {
    providers: [
        {
            provide: BACKEND_URL,
            useValue:
                'https://photoapp.looknongmodules.com/api',
        },
        provideRouter([
            /* app routes */
        ]),
        // ...
    ],
});
```

Многие сторонние библиотеки также были обновлены для поддержки этого шаблона конфигурации `provide`-функции. Если библиотека предлагает только API `NgModule` для конфигурации DI, вы можете использовать утилиту `importProvidersFrom`, чтобы по-прежнему использовать ее в `bootstrapApplication` и других автономных контекстах:

```ts
import { LibraryModule } from 'ngmodule-based-library';
bootstrapApplication(PhotoAppComponent, {
    providers: [
        {
            provide: BACKEND_URL,
            useValue:
                'https://photoapp.looknongmodules.com/api',
        },
        importProvidersFrom(LibraryModule.forRoot()),
    ],
});
```

## Маршрутизация и ленивая загрузка

API маршрутизатора были обновлены и упрощены, чтобы использовать преимущества автономных компонентов: `NgModule` больше не требуется во многих распространенных сценариях ленивой загрузки.

### Ленивая загрузка отдельного компонента

Любой маршрут может лениво загрузить свой маршрутизируемый отдельный компонент, используя `loadComponent`:

```ts
export const ROUTES: Route[] = [
    {
        path: 'admin',
        loadComponent: () =>
            import('./admin/panel.component').then(
                (mod) => mod.AdminPanelComponent
            ),
    },
    // ...
];
```

Это работает до тех пор, пока загружаемый компонент является автономным.

### Ленивая загрузка множества маршрутов одновременно

Операция `loadChildren` теперь поддерживает загрузку нового набора дочерних `маршрутов` без необходимости писать лениво загружаемый `NgModule`, который импортирует `RouterModule.forChild` для объявления маршрутов. Это работает, когда каждый маршрут, загруженный таким образом, использует отдельный компонент.

```ts
// In the main application:
export const ROUTES: Route[] = [
    {
        path: 'admin',
        loadChildren: () =>
            import('./admin/routes').then(
                (mod) => mod.ADMIN_ROUTES
            ),
    },
    // ...
];

// In admin/routes.ts:
export const ADMIN_ROUTES: Route[] = [
    { path: 'home', component: AdminHomeComponent },
    { path: 'users', component: AdminUsersComponent },
    // ...
];
```

### Ленивая загрузка и экспорты по умолчанию

При использовании `loadChildren` и `loadComponent` маршрутизатор понимает и автоматически разворачивает динамические вызовы `import()` с `default` экспортом. Вы можете воспользоваться этим, чтобы пропустить `.then()` для таких операций ленивой загрузки.

```ts
// In the main application:
export const ROUTES: Route[] = [
    {
        path: 'admin',
        loadChildren: () => import('./admin/routes'),
    },
    // ...
];

// In admin/routes.ts:
export default [
    { path: 'home', component: AdminHomeComponent },
    { path: 'users', component: AdminUsersComponent },
    // ...
] as Route[];
```

### Предоставление услуг подмножеству маршрутов

API ленивой загрузки для `NgModule` (`loadChildren`) создает новый инжектор "модуля", когда загружает лениво загруженные дочерние элементы маршрута. Эта возможность часто была полезна для предоставления услуг только подмножеству маршрутов в приложении. Например, если все маршруты под `/admin` были скопированы с помощью границы `loadChildren`, то сервисы только для администраторов могли быть предоставлены только этим маршрутам. Для этого требовалось использовать API `loadChildren`, даже если ленивая загрузка соответствующих маршрутов не требовалась.

Теперь Router поддерживает явное указание дополнительных `провайдеров` в `маршруте`, что позволяет сделать такую же привязку без ленивой загрузки или `NgModule`. Например, скопированные сервисы в структуре маршрута `/admin` будут выглядеть следующим образом:

```ts
export const ROUTES: Route[] = [
    {
        path: 'admin',
        providers: [
            AdminService,
            { provide: ADMIN_API_KEY, useValue: '12345' },
        ],
        children: [
            {
                path: 'users',
                component: AdminUsersComponent,
            },
            {
                path: 'teams',
                component: AdminTeamsComponent,
            },
        ],
    },
    // ... other application routes that don't
    //     have access to ADMIN_API_KEY or AdminService.
];
```

Также можно комбинировать `providers` с `loadChildren` дополнительной конфигурации маршрутизации, чтобы достичь того же эффекта ленивой загрузки `NgModule` с дополнительными маршрутами и провайдерами на уровне маршрутов. В этом примере настраиваются те же провайдеры/детские маршруты, что и выше, но за границей ленивой загрузки:

```ts
// Main application:
export const ROUTES: Route[] = {
  // Lazy-load the admin routes.
  {
	path: 'admin',
	loadChildren: () => import('./admin/routes').then(
		mod => mod.ADMIN_ROUTES
	)
  },
  // ... rest of the routes
}

// In admin/routes.ts:
export const ADMIN_ROUTES: Route[] = [{
  path: '',
  pathMatch: 'prefix',
  providers: [
    AdminService,
    {provide: ADMIN_API_KEY, useValue: 12345},
  ],
  children: [
    {path: 'users', component: AdminUsersCmp},
    {path: 'teams', component: AdminTeamsCmp},
  ],
}];
```

Обратите внимание на использование маршрута с пустым путем для размещения `провайдеров`, которые являются общими для всех дочерних маршрутов.

`importProvidersFrom` можно использовать для импорта существующей конфигурации DI на основе NgModule в маршрутные `провайдеры`.

## Дополнительные темы

В этом разделе рассматриваются детали, которые относятся только к более продвинутым моделям использования. Вы можете смело пропустить этот раздел при первом знакомстве с автономными компонентами, директивами и трубами.

### Автономные компоненты для авторов библиотек

Автономные компоненты, директивы и трубы могут быть экспортированы из `NgModule`, которые их импортируют:

```ts
@NgModule({
    imports: [ImageCarouselComponent, ImageSlideComponent],
    exports: [ImageCarouselComponent, ImageSlideComponent],
})
export class CarouselModule {}
```

Этот шаблон полезен для библиотек Angular, которые публикуют набор взаимодействующих директив. В приведенном выше примере в шаблоне должны присутствовать `ImageCarouselComponent` и `ImageSlideComponent`, чтобы построить один логический "виджет карусели".

В качестве альтернативы публикации `NgModule`, авторы библиотек могут захотеть экспортировать массив взаимодействующих директив:

```ts
export const CAROUSEL_DIRECTIVES = [
    ImageCarouselComponent,
    ImageSlideComponent,
] as const;
```

Такой массив может быть импортирован приложениями, использующими `NgModule`, и добавлен в `@NgModule.imports`. Обратите внимание на наличие конструкции `as const` в TypeScript: она предоставляет компилятору Angular дополнительную информацию, необходимую для правильной компиляции, и является рекомендуемой практикой (поскольку делает экспортируемый массив неизменяемым с точки зрения TypeScript).

### Инъекция зависимостей и иерархия инжекторов

В приложениях Angular можно настроить инъекцию зависимостей, указав набор доступных провайдеров. В типичном приложении существует два различных типа инжекторов:

-   **модульный инжектор** с провайдерами, настроенными в `@NgModule.providers` или `@Injectable({providedIn: "..."})`. Эти общеприкладные провайдеры видны всем компонентам, а также другим сервисам, настроенным в инжекторе модуля.
-   **инжекторы узлов**, настроенные в `@Directive.providers` / `@Component.providers` или `@Component.viewProviders`. Эти провайдеры видны только для данного компонента и всех его дочерних компонентов.

#### Инжекторы среды

Сделать `NgModule` необязательным потребует новых способов конфигурирования инжекторов "модуля" с провайдерами для всего приложения (например, [HttpClient](https://angular.io/api/common/http/HttpClient)). В автономном приложении (созданном с помощью `bootstrapApplication`) провайдеры "модуля" могут быть настроены в процессе бутстрапа, в опции `providers`:

```ts
bootstrapApplication(PhotoAppComponent, {
    providers: [
        {
            provide: BACKEND_URL,
            useValue:
                'https://photoapp.looknongmodules.com/api',
        },
        { provide: PhotosService, useClass: PhotosService },
        // ...
    ],
});
```

Новый API bootstrap вернул нам возможность конфигурировать "инжекторы модулей" без использования `NgModule`. В этом смысле "модульная" часть названия больше не актуальна, и мы решили ввести новый термин: "инжекторы окружения".

Инжекторы окружения могут быть настроены с помощью одного из следующих способов:

-   `@NgModule.providers` (в приложениях, загружающихся через `NgModule`);
-   `@Injectable({provideIn: "..."})` (как в приложениях на основе NgModule, так и в "автономных" приложениях);
-   опция `providers` в вызове `bootstrapApplication` (в полностью "автономных" приложениях);
-   поле `providers` в конфигурации `Route`.

Angular v14 вводит новый тип TypeScript `EnvironmentInjector` для представления этого нового именования. Сопутствующий API `createEnvironmentInjector` позволяет создавать инжекторы окружения программно:

```ts
import { createEnvironmentInjector } from '@angular/core';

const parentInjector = … // existing environment injector
const childInjector = createEnvironmentInjector(
    [
        {
            provide: PhotosService,
            useClass: CustomPhotosService,
        },
    ],
    parentInjector
);
```

Инжекторы среды имеют одну дополнительную возможность: они могут выполнять логику инициализации при создании инжектора среды (аналогично конструкторам `NgModule`, которые выполняются при создании инжектора модуля):

```ts
import {
    createEnvironmentInjector,
    ENVIRONMENT_INITIALIZER,
} from '@angular/core';
createEnvironmentInjector([
    {
        provide: PhotosService,
        useClass: CustomPhotosService,
    },
    {
        provide: ENVIRONMENT_INITIALIZER,
        useValue: () => {
            console.log(
                'This function runs when this EnvironmentInjector gets created'
            );
        },
    },
]);
```

#### Автономные инжекторы

В действительности иерархия инжекторов зависимостей в приложениях, использующих автономные компоненты, несколько более сложна. Рассмотрим следующий пример:

```ts
// an existing "datepicker" component with an NgModule
@Component({
        selector: 'datepicker',
        template: '...',
})
class DatePickerComponent {
  constructor(private calendar: CalendarService) {}
}

@NgModule({
        declarations: [DatePickerComponent],
        exports: [DatePickerComponent]
        providers: [CalendarService],
})
class DatePickerModule {
}

@Component({
        selector: 'date-modal',
        template: '<datepicker></datepicker>',
        standalone: true,
        imports: [DatePickerModule]
})
class DateModalComponent {
}
```

В приведенном выше примере компонент `DateModalComponent` является автономным - он может быть использован напрямую и не имеет `NgModule`, который должен быть импортирован для его использования. Однако `DateModalComponent` имеет зависимость, `DatePickerComponent`, которая импортируется через свой `NgModule` (`DatePickerModule`). Этот `NgModule` может объявлять провайдеров (в данном случае: `CalendarService`), которые необходимы для правильной работы `DatePickerComponent`.

Когда Angular создает отдельный компонент, ему необходимо знать, что текущий инжектор имеет все необходимые сервисы для зависимостей отдельного компонента, включая те, которые основаны на `NgModules`. Чтобы гарантировать это, в некоторых случаях Angular создает новый "автономный инжектор" в качестве дочернего инжектора текущего окружения. Сегодня это происходит для всех загружаемых автономных компонентов: они будут дочерними по отношению к инжектору корневого окружения. Это же правило применяется к динамически создаваемым (например, маршрутизатором или API `ViewContainerRef`) автономным компонентам.

Отдельный инжектор автономного компонента создается для того, чтобы провайдеры, импортируемые автономным компонентом, были "изолированы" от остальной части приложения. Это позволяет нам рассматривать автономные компоненты как действительно самодостаточные части, которые не могут "сливать" детали своей реализации остальному приложению.

#### Разрешение циклических зависимостей с помощью прямой ссылки на класс

Порядок объявления классов имеет значение в TypeScript. Вы не можете напрямую ссылаться на класс, пока он не определен.

Обычно это не является проблемой, но иногда круговые ссылки неизбежны. Например, когда класс 'A' ссылается на класс 'B', а 'B' ссылается на 'A'. Один из них должен быть определен первым.

Функция Angular `forwardRef()` создает косвенную ссылку, которую Angular может разрешить позже.

Например, такая ситуация возникает, когда отдельный родительский компонент импортирует отдельный дочерний компонент и наоборот. Вы можете решить эту проблему круговой зависимости с помощью функции `forwardRef`.

```ts
@Component({
    standalone: true,
    imports: [ChildComponent],
    selector: 'app-parent',
    template: `<app-child
        [hideParent]="hideParent"
    ></app-child>`,
})
export class ParentComponent {
    @Input() hideParent: boolean;
}

@Component({
    standalone: true,
    imports: [
        CommonModule,
        forwardRef(() => ParentComponent),
    ],
    selector: 'app-child',
    template: `<app-parent
        *ngIf="!hideParent"
    ></app-parent>`,
})
export class ChildComponent {
    @Input() hideParent: boolean;
}
```

!!!warning ""

    Такой импорт может привести к бесконечной рекурсии во время инстанцирования компонента. Убедитесь, что эта рекурсия имеет условие выхода, которое останавливает ее в определенный момент.
