import com.sun.net.httpserver.HttpServer;
import java.io.OutputStream;
import java.net.InetSocketAddress;

/**
 * Fausse API "Spring Boot" : 30 lignes, aucune dependance.
 * Elle expose /actuator/health et /api/message, lit sa configuration dans
 * l'environnement, et s'arrete proprement sur SIGTERM.
 * Le but des labos est Docker, pas Java : ce fichier ne change jamais.
 */
public class Api {
    public static void main(String[] args) throws Exception {
        int port = Integer.parseInt(env("SERVER_PORT", "8080"));
        String message = env("APP_MESSAGE", "Bonjour depuis l'API");
        String profile = env("APP_PROFILE", "default");

        System.out.println("Arguments recus : " + (args.length == 0 ? "(aucun)" : String.join(" ", args)));

        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
        server.createContext("/actuator/health", ex -> send(ex.getResponseBody(), ex, "{\"status\":\"UP\"}"));
        server.createContext("/", ex -> send(ex.getResponseBody(), ex,
                "{\"message\":\"" + message + "\",\"profile\":\"" + profile + "\"}"));
        server.start();
        System.out.println("API demarree sur le port " + port + " (profil " + profile + ")");

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.out.println("SIGTERM recu : arret propre en cours...");
            server.stop(2);
            System.out.println("API arretee proprement.");
        }));
    }

    private static String env(String name, String defaut) {
        String v = System.getenv(name);
        return (v == null || v.isEmpty()) ? defaut : v;
    }

    private static void send(OutputStream body, com.sun.net.httpserver.HttpExchange ex, String json) throws java.io.IOException {
        byte[] data = json.getBytes("UTF-8");
        ex.getResponseHeaders().add("Content-Type", "application/json");
        ex.sendResponseHeaders(200, data.length);
        body.write(data);
        body.close();
    }
}
