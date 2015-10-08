import java.net.ServerSocket;
import java.net.Socket;

import java.io.IOException;

public class Server {

  // we'll just use this to keep a counter of our requests.
  private static int counter = 0;
  
  public static void main(String[] args) throws IOException {

    // we open a server socket...
    ServerSocket serverSocket = new ServerSocket(8080);
    
    // ... and wait.
    Socket clientConnection = serverSocket.accept();

    while (clientConnection != null) {
      // we process each connection as they come in.
      processConnection(clientConnection);

      clientConnection = serverSocket.accept();
    }
    
    // note that we never actually close this gracefully - you'll have to use Ctrl+C to quit.
  }

  private static void processConnection(Socket client) throws IOException {
    System.out.println("Processing client...");
    
    // create a request
    HttpRequest request = new HttpRequest(client.getInputStream());
    
    // create a response
    HttpResponse response = new HttpResponse(client.getOutputStream());

    // handle the request here.  you could serve a file, you could create some JSON, map requests to different handler classes... whatever you need.
    handleRequest(request, response);

    response.getWriter().close();
    client.close();
    
    System.out.println("Client processed.");
  }

  private static void handleRequest(HttpRequest request, HttpResponse response) throws IOException {
    // our simple handler will just output a message to the user.
    response.getWriter().write("<html><body>Everything is OK.<input type=\"hidden\" value=\"" + counter++ + "\"></body></html>");
  }
}
