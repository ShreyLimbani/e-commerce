import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
})
export class CartComponent implements OnInit {
  cart: any = [];
  totalAmount: number = 0;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.loadCart();
  }

  loadCart() {
    this.apiService.viewCart('user1').subscribe((data) => {
      this.cart = data.cart;
      this.totalAmount = data.total_amount;
    });
  }
}
