
package inheritance;

import java.net.*;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import org.apache.xmlrpc.XmlRpcException;
import org.concordion.integration.junit3.ConcordionTestCase;
import org.concordion.api.ExpectedToPass;
import java.lang.reflect.Array;
import java.util.*;

@ExpectedToPass
public class Utilities extends ConcordionTestCase{

    XmlRpcClient client = null;

    public void setUp() throws MalformedURLException{
        XmlRpcClientConfigImpl config = new XmlRpcClientConfigImpl();
        config.setServerURL(new URL("http://localhost:1337/"));
        this.client = new XmlRpcClient();
        this.client.setConfig(config);
    }
public Object getGreetings(String name) throws XmlRpcException{
    Object result = this.client.execute("Utilities_getGreetings", new Object[]{name});
    if(result.getClass().isArray()){
        List<Object> list = new ArrayList<Object>();
        for(int i = 0; i < Array.getLength(result); i++){
            list.add(Array.get(result, i));
        }
        return list;
    }
    return result;
}
}