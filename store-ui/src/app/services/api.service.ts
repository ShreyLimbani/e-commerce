import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private baseUrl = 'http://localhost:8000/api'; // Your backend URL

  constructor(private http: HttpClient) {}

  // Items
  listItems(): Observable<any> {
    return this.http.get(`${this.baseUrl}/items/`);
  }

  addItem(itemData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/admin/add-item/`, itemData);
  }

  // Cart
  addToCart(cartData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/cart/add/`, cartData);
  }

  viewCart(userId: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/cart/view/${userId}`);
  }

  checkout(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/cart/checkout/`, data);
  }

  // Admin
  generateDiscount(discountData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/admin/generate-discount/`, discountData);
  }

  viewStats(): Observable<any> {
    return this.http.get(`${this.baseUrl}/admin/stats/`);
  }
}
