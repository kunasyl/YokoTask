Для создания заказа `orders/create/?phone_number=+77774556677`:
```JSON
{
    "start_date":"2022-12-31T23:59:59",
    "end_date":"2022-12-31T23:59:59",
    "store_id":1,
    "customer_id":1,
    "status":"started",
    "employee_id":1
}
```

Для создания посещения `visits/create/?phone_number=+77774556677`
```JSON
{
    "start_date":"2023-10-31T23:59:59",
    "employee_id":1,
    "order_id":2,
    "customer_id":2,
    "store_id":2
}
```
 Для обновления - `visits/<int:pk>/update/?phone_number=+77774556677`
 
Для просмотра торговых точек - `stores/?phone_number=+77774556677`