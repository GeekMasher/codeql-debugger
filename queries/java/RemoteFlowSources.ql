import java
import semmle.code.java.dataflow.FlowSources

from DataFlow::Node s
where s instanceof RemoteFlowSource
select s
