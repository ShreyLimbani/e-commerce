import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
    <nav>
      <a routerLink="/">Items</a> |
      <a routerLink="/cart">Cart</a> |
      <a routerLink="/checkout">Checkout</a> |
      <a routerLink="/admin">Admin</a>
    </nav>
    <router-outlet></router-outlet>
  `,
})
export class AppComponent {}
