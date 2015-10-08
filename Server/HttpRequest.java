import java.util.*;
import java.io.*;

public class HttpRequest {

  // we'll just use these constants to refer to these strings later.
  private static final String HTTP = "HTTP/1.1";
  private static final String GET = "GET ";
  private static final String POST = "POST ";

  // we'll store this for GET 
  private String requestMethod;
  
  // This map will hold all of the headers we parse
  private Map<String, String> headers = new HashMap<String, String>();
  
  // This map will hold all of our parameters.
  private Map<String, List<String>> parameters = new HashMap<String, List<String>>();
  
  // This is the document requested 
  private String document;

  public HttpRequest(InputStream input) throws IOException {
    BufferedReader in = new BufferedReader(new InputStreamReader(input));
    
    // we'll read the first line
    String line = in.readLine();
    if (line != null) {
    
      // the first line will be GET
      if (line.startsWith(GET)) {
        // parameters on the URL, so we'll need to parse those.
        if (line.endsWith(HTTP)) {
        
          // let's parse the doc
          String doc = line.substring(GET.length(), line.length() - HTTP.length());
          
          // we'll parse the parameters next
          int question = doc.indexOf("?");
          if (question >= 0) {
            String paramText = doc.substring(question + 1);
            processParameters(paramText);
            this.document = doc.substring(0, question);
          } else {
            this.document = doc;
          }
        } else {
          throw new IOException("001: Problem reading HTTP header.");
        }
        requestMethod = "GET";

        parseHeaders(in);
      }
      // if it's not GET, we're not handling it here.
    }
  }

  // note that we might end up with a list of parameter values - we parse the list here
  private void processParameters(String paramText) {
    String[] params = paramText.split("&");
    for (String param : params) {
      int equals = param.indexOf("=");
      if (equals >= 0) {
        addParameter(param.substring(0, equals), param.substring(equals + 1));
      } else {
        addParameter(param, "");
      }
    }
  }

  private void addParameter(String name, String value) {
    List<String> values = parameters.get(name);
    if (values == null) {
      values = new ArrayList<String>(2);
      parameters.put(name, values);
    }
    values.add(value);
  }

  public String getHeader(String header) {
    return headers.get(header);
  }

  public String getParameter(String name) {
    String result = null;
    List<String> values = getParameters(name);
    if (values != null) {
      result = values.get(0);
    }
    return result;
  }

  public List<String> getParameters(String name) {
    return parameters.get(name);
  }

  private void parseHeader(String line) {
    int index = line.indexOf(": ");
    if (index >= 0) {
      String header = line.substring(0, index);
      String value = line.substring(index + 2);
      headers.put(header, value);
    }
  }

  private void parseHeaders(BufferedReader in) throws IOException {
    String line = in.readLine();
    while (line != null && !line.trim().equals("")) {
      parseHeader(line);
      line = in.readLine();
    }
  }
}
