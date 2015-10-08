import java.io.*;
import java.util.*;

public class HttpResponse {

  private Writer out;
  private Map<String, String> headers = new HashMap<String, String>();
  private boolean headersWritten = false;

  public HttpResponse(OutputStream outputStream) {
    out = new OutputStreamWriter(outputStream);
  }

  // we'll allow the user to set response headers.
  public void setHeader(String name, String value) throws IOException {
    if (headersWritten) {
      throw new IOException("002: HTTP headers already written to output.");
    }
    headers.put(name, value);
  }

  private void writeHeaders() throws IOException {
    for (String header : headers.keySet()) {
      out.write(header);
      out.write(": ");
      out.write(headers.get(header));
      out.write("\n");
    }
    out.write("\n");
    headersWritten = true;
  }
  
  // we'll need to write the headers first.  we want to make sure these come before content.
  public Writer getWriter() throws IOException {
    if (!headersWritten) {
      writeHeaders();
    }
    return out;
  }
}
