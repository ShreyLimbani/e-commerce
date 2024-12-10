import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-checkout',
  templateUrl: './checkout.component.html',
})
export class CheckoutComponent {
  discountCode: string = '';

  constructor(private apiService: ApiService) {}

  checkout() {
    const data = { user_id: 'user1', discount_code: this.discountCode };
    this.apiService.checkout(data).subscribe((response) => {
      alert('Order Placed! Final Amount: ' + response.final_amount);
      if (response.new_discount_code) {
        alert('New Discount Code: ' + response.new_discount_code);
      }
    });
  }
}
