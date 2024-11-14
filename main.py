from http.server import BaseHTTPRequestHandler, HTTPServer

# Для начала определим настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    """
    Специальный класс, который отвечает за
    обработку входящих запросов от клиентов
    """

    def do_GET(self):
        """ Метод для обработки GET-запросов """
        if self.path == "/favicon.ico":
            self.send_response(204)  # Отправляем успешный ответ без контента
            self.end_headers()
            return

        # Остальная обработка запросов
        path = self.get_path()
        print(f"Requested path: {path}")
        try:
            with open(path, "r", encoding="utf-8") as file:
                page_content = file.read()
        except FileNotFoundError:
            self.send_error(404, "File Not Found")
        else:
            self.send_response(200)  # Отправка кода ответа
            self.send_header("Content-type", self.get_content_type())  # Отправка типа данных
            self.end_headers()  # Завершение формирования заголовков ответа
            self.wfile.write(bytes(page_content, "utf-8"))  # Тело ответа

    def get_path(self) -> str:
        if self.path == "/":
            return "home_page.html"
        return self.path[1:]

    def get_content_type(self) -> str:
        if self.path.endswith(".css"):
            return "text/css"
        elif self.path.endswith(".js"):
            return "text/javascript"
        else:
            return "text/html"


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")
