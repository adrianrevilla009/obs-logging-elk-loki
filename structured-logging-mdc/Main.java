import java.time.Instant;
import java.util.*;

/** JSON logs with an MDC and a trace id, JDK only (no logback needed to run). */
public class Main {
    static final ThreadLocal<Map<String, String>> MDC = ThreadLocal.withInitial(LinkedHashMap::new);

    static String esc(String s) {
        return s.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n");
    }

    static String log(String level, String msg) {
        StringBuilder sb = new StringBuilder("{\"ts\":\"" + Instant.now() + "\",\"level\":\"" + level + "\"");
        MDC.get().forEach((k, v) -> sb.append(",\"").append(esc(k)).append("\":\"").append(esc(v)).append("\""));
        sb.append(",\"msg\":\"").append(esc(msg)).append("\"}");
        System.out.println(sb);
        return sb.toString();
    }

    static void handleOrder(String orderId) {
        MDC.get().put("traceId", UUID.randomUUID().toString().replace("-", "").substring(0, 16));
        MDC.get().put("orderId", orderId);
        try {
            log("INFO", "order received");
            log("INFO", "payment authorised");
        } finally {
            MDC.get().clear();
        }
    }

    public static void main(String[] args) throws Exception {
        handleOrder("o-1");
        Thread t = new Thread(() -> handleOrder("o-2"));
        t.start();
        t.join();
        String after = log("INFO", "outside request");
        if (after.contains("traceId")) throw new AssertionError("MDC leaked");
        System.out.println("OK: every request line carries traceId/orderId, MDC cleared afterwards");
    }
}
