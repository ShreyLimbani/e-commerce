import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-item-list',
  templateUrl: './item-list.component.html',
})
export class ItemListComponent implements OnInit {
  items: any[] = [];

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.loadItems();
  }

  loadItems() {
    this.apiService.listItems().subscribe((data) => {
      this.items = data;
    });
  }

  addToCart(itemId: string) {
    const cartData = { user_id: 'user1', item_id: itemId, quantity: 1 };
    this.apiService.addToCart(cartData).subscribe(() => {
      alert('Item added to cart!');
    });
  }
}
