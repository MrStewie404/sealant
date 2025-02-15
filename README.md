# sealant
При работе над проектом запуск сервера производился с использованием команды:
<br>
<code> python manage.py runserver </code>
<br>
<br>
В моём проекте всё взаимодействие с сервером реализовано через websocket соединение. Поэтому для получения таблиц требуется запуск uvicorn. 
<br>
Команда для запуска:
<br>
<code> uvicorn Project.asgi:application --host localhost --port 9090 </code>
При успешном соединении, на страницу в консоли браузера будет выведено сообщение <i>WebSocket connection opened</i>
<br>
<br>
Логины: admin2, client, service_organization, manager
<br>Пароль (для всех): Password01
<br>
<br>
<i>Скриншоты:</i>

#### Главная страница
##### Расположение: http://127.0.0.1:8000/
<img width="1680" alt="Снимок экрана 2025-02-15 в 20 10 39" src="https://github.com/user-attachments/assets/f1a93d06-f962-4320-bbfc-2d02b2979edf" />
<br>
<br>

#### Личный кабинет (если так можно назвать)
###### Расположение: http://127.0.0.1:8000/accounts/profile/machines/ (скриншот 2)
###### При пустых полях сервер отправляет все имеющиеся сущности в выбранной таблице (сделано с ориентиром на удобство использования)
###### Также хотел бы заметить, что для сортировки не требуется ввод значений, а сама сортировка производится на сервере, средствами Django
<div style="display: flex; flex-direction: row; width: 100%">
  <img width="75%" alt="изображение" src="https://github.com/user-attachments/assets/593d301c-ea28-4b10-9e9c-1b46c7510325" />
  <img width="20%" alt="изображение" src="https://github.com/user-attachments/assets/4789cafd-79c4-48b3-98cc-8fcbb99d0c92" />
</div>
<br>
<br>

#### Пример страницы создания сущности
###### Расположение: http://127.0.0.1:8000/create/machine/ (скриншот 3)
<div style="display: flex; flex-direction: row; width: 100%">
  <img width="75%" alt="изображение" src="https://github.com/user-attachments/assets/593d301c-ea28-4b10-9e9c-1b46c7510325" />
  <img width="20%" alt="изображение" src="https://github.com/user-attachments/assets/4789cafd-79c4-48b3-98cc-8fcbb99d0c92" />
</div>

