# Инъекция зависимостей в Angular

Когда вы разрабатываете небольшую часть системы, например, модуль или класс, вам может понадобиться использовать функции других классов. Например, вам может понадобиться HTTP-сервис для выполнения обращений к бэкенду. Инъекция зависимости (Dependency Injection, или DI) - это шаблон проектирования и механизм создания и передачи одних частей приложения другим частям приложения, которым они необходимы. Angular поддерживает этот шаблон проектирования, и вы можете использовать его в своих приложениях для повышения гибкости и модульности.

В Angular зависимости обычно представляют собой сервисы, но они также могут быть значениями, например, строками или функциями. Инжектор для приложения (создаваемый автоматически во время bootstrap) инстанцирует зависимости, когда это необходимо, используя настроенный поставщик сервиса или значения.

<div class="alert is-helpful">

Смотрите <live-example name="dependency-injection"></live-example> для рабочего примера, содержащего фрагменты кода из этого руководства.

</div>

## Предварительные условия

Вы должны быть знакомы с приложениями Angular в целом и иметь фундаментальные знания о компонентах, директивах и модулях NgModules. Настоятельно рекомендуем вам пройти следующий учебник:

[приложение и учебник Tour of Heroes](tutorial/tour-of-heroes)

## Узнайте об инъекции зависимостей Angular

<div class="card-container">
   <a href="guide/dependency-injection" class="docs-card" title="Understanding dependency injection">
    <section>Understanding dependency injection</section>
    <p>Learn basic principles of dependency injection in Angular.</p>
    <p class="card-footer">Understanding dependency injection</p>
  </a>
  <a href="guide/creating-injectable-service" class="docs-card" title="Creating and injecting service">
    <section>Creating and injecting service</section>
    <p>Describes how to create a service and inject it in other services and components.</p>
    <p class="card-footer">Creating an injectable service</p>
  </a>
  <a href="guide/dependency-injection-providers" class="docs-card" title="Configuring dependency providers">
    <section>Configuring dependency providers</section>
    <p>Describes how to configure dependencies using the providers field on the @Component and @NgModule decorators. Also describes how to use InjectionToken to provide and inject values in DI, which can be helpful when you want to use a value other than classes as dependencies.</p>
    <p class="card-footer">Configuring dependency providers</p>
  </a>
  <a href="guide/hierarchical-dependency-injection" class="docs-card" title="Hierarchical injectors">
    <section>Hierarchical injectors</section>
    <p>Hierarchical DI enables you to share dependencies between different parts of the application only when and if you need to. This is an advanced topic.</p>
    <p class="card-footer">Hierarchical injectors</p>
  </a>
</div>

:date: 2.08.2022
