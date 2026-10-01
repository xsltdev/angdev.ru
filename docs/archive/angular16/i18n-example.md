# Пример интернационализации приложения Angular

:date: 28.02.2022

## Изучите переведенный пример приложения

!!!note ""

    Чтобы изучить пример приложения с французским переводом, используемый в руководстве [Angular Internationalization][aioguidei18noverview], смотрите [пример](https://angular.io/generated/live-examples/i18n/stackblitz.html).

## пример `fr-CA` и `en-US`

На следующих вкладках отображается пример приложения и связанные с ним файлы перевода.

=== "src/app/app.component.html"

    ```html
    <h1
    	i18n="User welcome|An introduction header for this sample@@introductionHeader"
    >
    	Hello i18n!
    </h1>

    <ng-container i18n>I don't output any element</ng-container>

    <br />

    <img
    	[src]="logo"
    	i18n-title
    	title="Angular logo"
    	alt="Angular logo"
    />
    <br />
    <button type="button" (click)="inc(1)">+</button>
    <button type="button" (click)="inc(-1)">-</button>
    <span i18n
    	>Updated {minutes, plural, =0 {just now} =1 {one minute
    	ago} other {{{minutes}} minutes ago}}</span
    >
    ({{minutes}})
    <br /><br />
    <button type="button" (click)="male()">&#9794;</button>
    <button type="button" (click)="female()">&#9792;</button>
    <button type="button" (click)="other()">&#9895;</button>
    <span i18n
    	>The author is {gender, select, male {male} female
    	{female} other {other}}</span
    >
    <br /><br />
    <span i18n
    	>Updated: {minutes, plural, =0 {just now} =1 {one minute
    	ago} other {{{minutes}} minutes ago by {gender, select,
    	male {male} female {female} other {other}}}}
    </span>
    ```

=== "src/app/app.component.ts"

    ```ts
    import { Component } from '@angular/core';

    @Component({
    	selector: 'app-root',
    	templateUrl: './app.component.html',
    })
    export class AppComponent {
    	minutes = 0;
    	gender = 'female';
    	fly = true;
    	logo =
    		'https://angular.io/assets/images/logos/angular/angular.png';
    	inc(i: number) {
    		this.minutes = Math.min(
    			5,
    			Math.max(0, this.minutes + i)
    		);
    	}
    	male() {
    		this.gender = 'male';
    	}
    	female() {
    		this.gender = 'female';
    	}
    	other() {
    		this.gender = 'other';
    	}
    }
    ```

=== "src/app/app.module.ts"

    ```ts
    import { NgModule } from '@angular/core';
    import { BrowserModule } from '@angular/platform-browser';

    import { AppComponent } from './app.component';

    @NgModule({
    	imports: [BrowserModule],
    	declarations: [AppComponent],
    	bootstrap: [AppComponent],
    })
    export class AppModule {}
    ```

=== "src/main.ts"

    ```ts
    import { enableProdMode } from '@angular/core';
    import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

    import { AppModule } from './app/app.module';
    import { environment } from './environments/environment';

    if (environment.production) {
    	enableProdMode();
    }

    platformBrowserDynamic().bootstrapModule(AppModule);
    ```

=== "src/locale/messages.fr.xlf"

    ```xml
    <?xml version="1.0" encoding="UTF-8" ?>
    <xliff
    	version="1.2"
    	xmlns="urn:oasis:names:tc:xliff:document:1.2"
    >
    	<file
    		source-language="en"
    		datatype="plaintext"
    		original="ng2.template"
    	>
    		<body>
    			<trans-unit
    				id="introductionHeader"
    				datatype="html"
    			>
    				<source>Hello i18n!</source>
    				<note priority="1" from="description">
    					An introduction header for this sample
    				</note>
    				<note priority="1" from="meaning">
    					User welcome
    				</note>
    			</trans-unit>
    			<trans-unit
    				id="introductionHeader"
    				datatype="html"
    			>
    				<source>Hello i18n!</source>
    				<target>Bonjour i18n !</target>
    				<note priority="1" from="description">
    					An introduction header for this sample
    				</note>
    				<note priority="1" from="meaning">
    					User welcome
    				</note>
    			</trans-unit>
    			<trans-unit
    				id="ba0cc104d3d69bf669f97b8d96a4c5d8d9559aa3"
    				datatype="html"
    			>
    				<source
    				>I don&apos;t output any element</source>
    				<target>Je n'affiche aucun élément</target>
    			</trans-unit>
    			<trans-unit
    				id="701174153757adf13e7c24a248c8a873ac9f5193"
    				datatype="html"
    			>
    				<source>Angular logo</source>
    				<target>Logo d'Angular</target>
    			</trans-unit>
    			<trans-unit
    				id="5a134dee893586d02bffc9611056b9cadf9abfad"
    				datatype="html"
    			>
    				<source>
    					{VAR_PLURAL, plural, =0 {just now} =1
    					{one minute ago} other {
    					<x
    						id="INTERPOLATION"
    						equiv-text="{{minutes}}"
    					/>
    					minutes ago} }
    				</source>
    				<target>
    					{VAR_PLURAL, plural, =0 {à l'instant} =1
    					{il y a une minute} other {il y a
    					<x
    						id="INTERPOLATION"
    						equiv-text="{{minutes}}"
    					/>
    					minutes} }
    				</target>
    			</trans-unit>
    			<trans-unit
    				id="f99f34ac9bd4606345071bd813858dec29f3b7d1"
    				datatype="html"
    			>
    				<source>
    					The author is
    					<x
    						id="ICU"
    						equiv-text="{gender, select, male {...} female {...} other {...}}"
    					/>
    				</source>
    				<target>
    					L'auteur est
    					<x
    						id="ICU"
    						equiv-text="{gender, select, male {...} female {...} other {...}}"
    					/>
    				</target>
    			</trans-unit>
    			<trans-unit
    				id="eff74b75ab7364b6fa888f1cbfae901aaaf02295"
    				datatype="html"
    			>
    				<source>
    					{VAR_SELECT, select, male {male} female
    					{female} other {other} }
    				</source>
    				<target>
    					{VAR_SELECT, select, male {un homme}
    					female {une femme} other {autre} }
    				</target>
    			</trans-unit>
    			<trans-unit
    				id="972cb0cf3e442f7b1c00d7dab168ac08d6bdf20c"
    				datatype="html"
    			>
    				<source>
    					Updated:
    					<x
    						id="ICU"
    						equiv-text="{minutes, plural, =0 {...} =1 {...} other {...}}"
    					/>
    				</source>
    				<target>
    					Mis à jour:
    					<x
    						id="ICU"
    						equiv-text="{minutes, plural, =0 {...} =1 {...} other {...}}"
    					/>
    				</target>
    			</trans-unit>
    			<trans-unit
    				id="7151c2e67748b726f0864fc443861d45df21d706"
    				datatype="html"
    			>
    				<source>
    					{VAR_PLURAL, plural, =0 {just now} =1
    					{one minute ago} other {
    					<x
    						id="INTERPOLATION"
    						equiv-text="{{minutes}}"
    					/>
    					minutes ago by {VAR_SELECT, select, male
    					{male} female {female} other {other} }}
    					}
    				</source>
    				<target>
    					{VAR_PLURAL, plural, =0 {à l'instant} =1
    					{il y a une minute} other {il y a
    					<x
    						id="INTERPOLATION"
    						equiv-text="{{minutes}}"
    					/>
    					minutes par {VAR_SELECT, select, male
    					{un homme} female {une femme} other
    					{autre} }} }
    				</target>
    			</trans-unit>
    			<trans-unit id="myId" datatype="html">
    				<source>Hello</source>
    				<target state="new">Bonjour</target>
    			</trans-unit>
    		</body>
    	</file>
    </xliff>
    ```

<!-- links -->

[aioguidei18noverview]: i18n-overview.md

<!-- external links -->

<!-- end links -->
