import {
  ComponentFactoryResolver,
  Injectable,
  Inject,
  ViewContainerRef,
} from '@angular/core'

@Injectable()
export class DynamicComponentService {

  factoryResolver: ComponentFactoryResolver;
  rootViewContainer: ViewContainerRef;

  constructor(@Inject(ComponentFactoryResolver) factoryResolver) {
    this.factoryResolver = factoryResolver
  }

  setRootViewContainerRef(viewContainerRef) {
    this.rootViewContainer = viewContainerRef
  }

  addDynamicComponent(type: any) {
    const factory = this.factoryResolver.resolveComponentFactory(type)
    const component = factory.create(this.rootViewContainer.parentInjector)
    this.rootViewContainer.insert(component.hostView)
  }

}
