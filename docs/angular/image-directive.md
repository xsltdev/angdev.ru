# Getting started with NgOptimizedImage

The `NgOptimizedImage` directive makes it easy to adopt performance best practices for loading images.

The directive ensures that the loading of the [Largest Contentful Paint (LCP)](http://web.dev/lcp) image is prioritized by:

-   Automatically setting the `fetchpriority` attribute on the `<img>` tag

-   Lazy loading other images by default

-   Asserting that there is a corresponding preconnect link tag in the document head

-   Automatically generating a `srcset` attribute

-   Generating a [preload hint](https://developer.mozilla.org/en-US/docs/Web/HTML/Link_types/preload) if app is using SSR

In addition to optimizing the loading of the LCP image, `NgOptimizedImage` enforces a number of image best practices, such as:

-   Using [image CDN URLs to apply image optimizations](https://web.dev/image-cdns/#how-image-cdns-use-urls-to-indicate-optimization-options)

-   Preventing layout shift by requiring `width` and `height`

-   Warning if `width` or `height` have been set incorrectly

-   Warning if the image will be visually distorted when rendered

## Getting Started

#### Step 1: Import NgOptimizedImage

<code-example format="typescript" language="typescript">

import { NgOptimizedImage } from '@angular/common'

</code-example>

Директива определена как [отдельная директива](/guide/standalone-components), поэтому компоненты должны импортировать ее напрямую.

#### Шаг 2: (Необязательно) Настройка загрузчика

Загрузчик изображений не является **обязательным** для использования NgOptimizedImage, но его использование с CDN для изображений позволяет получить мощные возможности производительности, включая автоматический `srcset`s для ваших изображений.

Краткое руководство по настройке загрузчика можно найти в разделе [Configuring an Image Loader](#configuring-an-image-loader-for-ngoptimizedimage) в конце этой страницы.

#### Шаг 3: Включить директиву

Чтобы активировать директиву `NgOptimizedImage`, замените атрибут `src` вашего изображения на `ngSrc`.

<code-example format="typescript" language="typescript">

&lt;img ngSrc="cat.jpg"&gt;

</code-example>

Если вы используете [встроенный сторонний загрузчик](#built-in-loaders), не забудьте опустить путь к базовому URL из `src`, так как он будет добавлен автоматически загрузчиком.

#### Шаг 4: Пометьте изображения как `приоритетные`.

Всегда отмечайте [LCP изображение](https://web.dev/lcp/#what-elements-are-considered) на вашей странице как `приоритетное` для приоритетной загрузки.

<code-example format="typescript" language="typescript">

&lt;img ngSrc="cat.jpg" width="400" height="200" priority&gt;

</code-example>

Пометка изображения как `приоритетного` применяет следующие оптимизации:

-   Устанавливает `fetchpriority=high` (подробнее о приоритетных подсказках [здесь](https://web.dev/priority-hints)).

-   Устанавливает `loading=eager` (подробнее о нативной ленивой загрузке [здесь](https://web.dev/browser-level-image-lazy-loading)].

-   Автоматически генерирует элемент [preload link element](https://developer.mozilla.org/en-US/docs/Web/HTML/Link_types/preload), если [rendering on the server](/guide/universal).

Angular выводит предупреждение во время разработки, если LCP-элемент является изображением, у которого нет атрибута `priority`. LCP-элемент страницы может меняться в зависимости от ряда факторов - например, от размеров экрана пользователя, поэтому на странице может быть несколько изображений, которые должны иметь атрибут `priority`. Более подробную информацию см. в [CSS для веб-страниц](https://web.dev/css-web-vitals/#images-and-largest-contentful-paint-lcp).

#### Шаг 5: Укажите высоту и ширину.

Чтобы предотвратить [смещение макета, связанное с изображением] (https://web.dev/css-web-vitals/#images-and-layout-shifts), NgOptimizedImage требует, чтобы вы указали высоту и ширину изображения, как показано ниже:

<code-example format="typescript" language="typescript">

&lt;img ngSrc="cat.jpg" width="400" height="200"&gt;

</code-example>

Для **реагирующих изображений** (изображений, которые вы настроили на увеличение и уменьшение относительно области просмотра) атрибуты `width` и `height` должны соответствовать собственному размеру файла изображения.

Для изображений **фиксированного размера** атрибуты `width` и `height` должны отражать желаемый размер изображения. Соотношение сторон этих атрибутов всегда должно соответствовать внутреннему соотношению сторон изображения.

Примечание: Если вы не знаете размер ваших изображений, используйте "режим заполнения", чтобы унаследовать размер родительского контейнера, как описано ниже:

### Использование режима `fill`

В случаях, когда вы хотите, чтобы изображение заполняло содержащий его элемент, вы можете использовать атрибут `fill`. Это часто бывает полезно, когда вы хотите добиться поведения "фонового изображения". Он также может быть полезен, когда вы не знаете точную ширину и высоту изображения, но у вас есть родительский контейнер с известным размером, в который вы хотели бы поместить изображение (см. ниже "объектная подгонка").

Когда вы добавляете атрибут `fill` к своему изображению, вам не нужно и не следует указывать `width` и `height`, как в этом примере:

<code-example format="typescript" language="typescript">

&lt;img ngSrc="cat.jpg" fill&gt;

</code-example>

Вы можете использовать CSS-свойство [object-fit](https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit), чтобы изменить, как изображение будет заполнять свой контейнер. Если стилизовать изображение с помощью `object-fit: "contain"`, изображение сохранит соотношение сторон и будет "letterboxed", чтобы поместиться в элемент. Если задать `object-fit: "cover"`, элемент сохранит свое соотношение сторон, полностью заполнит элемент, а часть содержимого может быть "обрезана".

Смотрите наглядные примеры вышеописанного в [MDN object-fit documentation.](https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit).

Вы также можете изменить стиль изображения с помощью свойства [object-position](https://developer.mozilla.org/en-US/docs/Web/CSS/object-position), чтобы настроить его положение в содержащем его элементе.

**Важное замечание:** Чтобы изображение "fill" отображалось правильно, его родительский элемент \*\*должен быть стилизован с помощью `position: "relative"`, `position: "fixed"`, или `position: "`абсолютное`.

### Настройка стилизации изображения

В зависимости от стиля изображения, добавление атрибутов `width` и `height` может привести к тому, что изображение будет отображаться по-разному. `NgOptimizedImage` предупреждает вас, если ваш стиль изображения отображает его с искаженным соотношением сторон.

Обычно это можно исправить, добавив `height: auto` или `width: auto` в стили изображения. Для получения дополнительной информации см. статью [web.dev о теге `<img>`](https://web.dev/patterns/web-vitals-patterns/images/img-tag).

Если атрибуты `height` и `width` изображения не позволяют вам изменить размер изображения с помощью CSS, используйте режим "fill" и стилизуйте родительский элемент изображения.

## Особенности производительности

NgOptimizedImage включает в себя ряд функций, предназначенных для улучшения производительности загрузки в вашем приложении. Эти функции описаны в данном разделе.

### Добавить подсказки для ресурсов

Вы можете добавить [`preconnect` resource hint](https://web.dev/preconnect-and-dns-prefetch) для происхождения вашего изображения, чтобы гарантировать, что изображение LCP загрузится как можно быстрее. Всегда помещайте подсказки ресурсов в `<head>` документа.

<code-example format="html" language="html">

&lt;link rel="preconnect" href="https://my.cdn.origin" /&gt;

</code-example>

По умолчанию, если вы используете загрузчик для стороннего сервиса изображений, директива `NgOptimizedImage` будет предупреждать во время разработки, если обнаружит, что отсутствует подсказка ресурса `preconnect` для источника, обслуживающего LCP-образ.

Чтобы отключить эти предупреждения, введите маркер `PRECONNECT_CHECK_BLOCKLIST`:

<code-example format="typescript" language="typescript">

провайдеры: [ {provide: PRECONNECT_CHECK_BLOCKLIST, useValue: 'https://your-domain.com'}
],

</code-example>

### Запрашивать изображения нужного размера с помощью автоматического `srcset`.

Определение атрибута [`srcset`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/srcset) гарантирует, что браузер запросит изображение нужного размера для области просмотра пользователя, чтобы не тратить время на загрузку слишком большого изображения. `NgOptimizedImage` генерирует подходящий `srcset` для изображения, основываясь на наличии и значении атрибута [`sizes`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/sizes) в теге изображения.

#### Изображения фиксированного размера

Если ваше изображение должно быть "фиксированного" размера (т.е. одинакового размера на всех устройствах, за исключением [плотности пикселей](https://web.dev/codelab-density-descriptors/)), то нет необходимости устанавливать атрибут `sizes`. `srcset` может быть сгенерирован автоматически из атрибутов ширины и высоты изображения без необходимости дополнительного ввода.

Пример генерируемого srcset: `<img ... srcset="image-400w.jpg 1x, image-800w.jpg 2x">`.

#### Отзывчивые изображения

Если ваше изображение должно быть отзывчивым (т.е. увеличиваться и уменьшаться в зависимости от размера области просмотра), то вам необходимо определить атрибут [`sizes`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/sizes) для генерации `srcset`.

Если вы раньше не использовали `sizes`, то для начала лучше всего установить его на основе ширины области просмотра. Например, если ваш CSS заставляет изображение заполнять 100% ширины области просмотра, установите `sizes` в `100vw`, и браузер выберет изображение в `srcset`, которое ближе всего к ширине области просмотра (после учета плотности пикселей). Если ваше изображение будет занимать только половину экрана (например, в боковой панели), установите `sizes` в `50vw`, чтобы браузер выбрал изображение меньшего размера. И т.д.

Если вы обнаружили, что вышеперечисленное не соответствует желаемому поведению изображения, обратитесь к документации по [расширенным значениям размеров] (#advanced-sizes-values).

По умолчанию точками разрыва отзывчивости являются:

`[16, 32, 48, 64, 96, 128, 256, 384, 640, 750, 828, 1080, 1200, 1920, 2048, 3840]`

Если вы хотите настроить эти точки останова, вы можете сделать это с помощью провайдера `IMAGE_CONFIG`:

<code-example format="typescript" language="typescript"> providers: [
{
provide: IMAGE_CONFIG,
useValue: {
breakpoints: [16, 48, 96, 128, 384, 640, 750, 828, 1080, 1200, 1920]
}
},
],
</code-example>

Если вы хотите вручную определить атрибут `srcset`, вы можете задать свой собственный с помощью атрибута `ngSrcset`:

<code-example format="html" language="html">

&lt;img ngSrc="hero.jpg" ngSrcset="100w, 200w, 300w"&gt;

</code-example>

Если присутствует атрибут `ngSrcset`, `NgOptimizedImage` генерирует и устанавливает `srcset` на основе включенных размеров. Не включайте имена файлов изображений в `ngSrcset` - директива выводит эту информацию из `ngSrc`. Директива поддерживает как дескрипторы ширины (например, `100w`), так и дескрипторы плотности (например, `1x`).

<code-example format="html" language="html">

&lt;img ngSrc="hero.jpg" ngSrcset="100w, 200w, 300w" sizes="50vw"&gt;

</code-example>

### Отключение автоматической генерации srcset

Чтобы отключить генерацию srcset для отдельного изображения, вы можете добавить атрибут `disableOptimizedSrcset` к изображению:

<code-example format="html" language="html">

&lt;img ngSrc="about.jpg" disableOptimizedSrcset&gt;

</code-example>

### Отключение ленивой загрузки изображений

По умолчанию `NgOptimizedImage` устанавливает `loading=lazy` для всех изображений, которые не помечены как `приоритетные`. Вы можете отключить это поведение для неприоритетных изображений, установив атрибут `loading`. Этот атрибут принимает значения: `eager`, `auto` и `lazy`. [Подробнее см. документацию по стандартному атрибуту `loading` для изображений] (https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/loading#value).

<code-example format="html" language="html">

&lt;img ngSrc="cat.jpg" width="400" height="200" loading="eager"&gt;

</code-example>

### Расширенные значения 'sizes'

Вам может понадобиться отображать изображения разной ширины на экранах разного размера. Частым примером такой схемы является макет на основе сетки или колонок, который отображает одну колонку на мобильных устройствах и две колонки на больших устройствах. Вы можете описать это поведение в атрибуте `sizes`, используя синтаксис "медиазапроса", например, следующий:

<code-example format="html" language="html">

&lt;img ngSrc="cat.jpg" width="400" height="200" sizes="(max-width: 768px) 100vw, 50vw"&gt;

</code-example>

Атрибут `sizes` в приведенном выше примере говорит: "Я ожидаю, что это изображение будет занимать 100 процентов ширины экрана на устройствах шириной менее 768px. В противном случае я ожидаю, что оно будет занимать 50 процентов ширины экрана".

Дополнительную информацию об атрибуте `sizes` смотрите в [web.dev](https://web.dev/learn/design/responsive-images/#sizes) или [mdn](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/sizes).

## Настройка загрузчика изображений для `NgOptimizedImage`.

Загрузчик" - это функция, которая генерирует [URL преобразования изображения](https://web.dev/image-cdns/#how-image-cdns-use-urls-to-indicate-optimization-options) для заданного файла изображения. Когда это необходимо, `NgOptimizedImage` устанавливает размер, формат и качество преобразования изображения.

`NgOptimizedImage` предоставляет как общий загрузчик, который не применяет никаких преобразований, так и загрузчики для различных сторонних сервисов изображений. Он также поддерживает написание собственного пользовательского загрузчика.

| Тип загрузчика | Поведение | | :------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Общий загрузчик | URL, возвращаемый общим загрузчиком, всегда будет совпадать со значением `src`. Другими словами, этот загрузчик не применяет никаких преобразований. Сайты, использующие Angular для работы с изображениями, являются основным вариантом использования этого загрузчика. |

| Загрузчики для сторонних сервисов изображений | URL, возвращаемый загрузчиками для сторонних сервисов изображений, будет следовать соглашениям API, используемым этим конкретным сервисом изображений. |

| Пользовательские загрузчики | Поведение пользовательского загрузчика определяется его разработчиком. Вы должны использовать пользовательский загрузчик, если ваш сервис изображений не поддерживается загрузчиками, которые поставляются с `NgOptimizedImage`. |

Основываясь на сервисах изображений, обычно используемых в приложениях Angular, `NgOptimizedImage` предоставляет загрузчики, предварительно настроенные для работы со следующими сервисами изображений:

| Сервис изображений | Angular API | Документация | :------------------------ | :------------------------ | :-------------------------------------------------------------------------- | |
| Cloudflare Image Resizing | `provideCloudflareLoader` | [Документация](https://developers.cloudflare.com/images/image-resizing/)|

| Cloudinary | `provideCloudinaryLoader` | [Документация](https://cloudinary.com/documentation/resizing_and_cropping)|

| ImageKit | `provideImageKitLoader` | [Документация](https://docs.imagekit.io/)| |

| Imgix | `provideImgixLoader` | [Документация](https://docs.imgix.com/)|.

Для использования **генеративного загрузчика** не требуется никаких дополнительных изменений кода. Это поведение по умолчанию.

### Встроенные загрузчики

Чтобы использовать существующий загрузчик для **стороннего сервиса изображений**, добавьте фабрику провайдеров для выбранного вами сервиса в массив `providers`. В примере ниже используется загрузчик Imgix:

<code-example format="typescript" language="typescript"> providers: [
provideImgixLoader('https://my.base.url/'),
],
</code-example>

Базовый URL для ваших активов изображений должен быть передан фабрике провайдера в качестве аргумента. Для большинства сайтов этот базовый URL должен соответствовать одному из следующих шаблонов:

-   https://yoursite.yourcdn.com

-   https://subdomain.yoursite.com

-   https://subdomain.yourcdn.com/yoursite

Подробнее о структуре базового URL вы можете узнать в документации соответствующего CDN-провайдера.

### Пользовательские загрузчики

Чтобы использовать **настраиваемый загрузчик**, предоставьте свою функцию загрузчика в качестве значения для DI-токена `IMAGE_LOADER`. В приведенном ниже примере пользовательская функция загрузчика возвращает URL, начинающийся с `https://example.com`, который включает `src` и `width` в качестве параметров URL.

<code-example format="typescript" language="typescript"> providers: [
{
provide: IMAGE_LOADER,
useValue: (config: ImageLoaderConfig) => {
return `https://example.com/images?src=${config.src}&width=${config.width}`;
},
},
],
</code-example>

Функция загрузчика для директивы `NgOptimizedImage` принимает в качестве аргумента объект с типом `ImageLoaderConfig` (из `@angular/common`) и возвращает абсолютный URL актива изображения. Объект `ImageLoaderConfig` содержит свойство `src`, а также необязательные свойства `width` и `loaderParams`.

Примечание: хотя свойство `width` может присутствовать не всегда, пользовательский загрузчик должен использовать его для поддержки запроса изображений различной ширины, чтобы `ngSrcset` работал правильно.

### Свойство `loaderParams`.

Существует дополнительный атрибут, поддерживаемый директивой `NgOptimizedImage`, называемый `loaderParams`, который специально разработан для поддержки использования пользовательских загрузчиков. Атрибут `loaderParams` принимает в качестве значения объект с любыми свойствами и сам по себе ничего не делает. Данные в `loaderParams` добавляются в объект `ImageLoaderConfig`, передаваемый вашему пользовательскому загрузчику, и могут быть использованы для управления поведением загрузчика.

Чаще всего `loaderParams` используется для управления расширенными возможностями CDN для изображений.

### Пример пользовательского загрузчика

Ниже показан пример функции пользовательского загрузчика. Эта функция конкатенирует `src` и `width` и использует `loaderParams` для управления функцией CDN для закругленных углов:

<code-example format="typescript" language="typescript"> const myCustomLoader = (config: ImageLoaderConfig) => {
let url = `https://example.com/images/${config.src}?`;
let queryParams = [];
if (config.width) {
queryParams.push(`w=${config.width}`);
}
if (config.loaderParams?.roundedCorners) {
queryParams.push('mask=corners&corner-radius=5');
}
return url + queryParams.join('&');
};
</code-example>

Обратите внимание, что в приведенном выше примере мы придумали имя свойства 'roundedCorners' для управления функцией нашего пользовательского загрузчика. Затем мы можем использовать это свойство при создании изображения, как показано ниже:

<code-example format="html" language="html">

&lt;img ngSrc="profile.jpg" width="300" height="300" [loaderParams]="{roundedCorners: true}"&gt;

</code-example>

<!-- links -->

<!-- external links -->

<!--end links -->

:date: 7.11.2022
