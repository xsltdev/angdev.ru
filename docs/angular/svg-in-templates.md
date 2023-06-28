# SVG как шаблоны

:date: 28.02.2022

Вы можете использовать файлы SVG в качестве шаблонов в своих приложениях Angular. Когда вы используете SVG в качестве шаблона, вы можете использовать директивы и привязки так же, как и в шаблонах HTML.

Используйте эти возможности для динамической генерации интерактивной графики.

!!!note ""

    Смотрите [код](https://angular.io/generated/live-examples/template-syntax/stackblitz.html) для рабочего примера, содержащего фрагменты кода из этого руководства.

## Пример синтаксиса SVG

В следующем примере показан синтаксис для использования SVG в качестве шаблона.

```ts
import { Component } from '@angular/core';

@Component({
    selector: 'app-svg',
    templateUrl: './svg.component.svg',
    styleUrls: ['./svg.component.css'],
})
export class SvgComponent {
    fillColor = 'rgb(255, 0, 0)';

    changeColor() {
        const r = Math.floor(Math.random() * 256);
        const g = Math.floor(Math.random() * 256);
        const b = Math.floor(Math.random() * 256);
        this.fillColor = `rgb(${r}, ${g}, ${b})`;
    }
}
```

Чтобы увидеть привязку свойств и событий в действии, добавьте следующий код в файл `svg.component.svg`:

```xml
<svg>
  <g>
    <rect
		x="0" y="0" width="100" height="100"
		[attr.fill]="fillColor" (click)="changeColor()" />
    <text x="120" y="50">
		click the rectangle to change the fill color
	</text>
  </g>
</svg>
```

В приведенном примере используется привязка события `click()` и синтаксис привязки свойства (`[attr.fill]="fillColor"`).
