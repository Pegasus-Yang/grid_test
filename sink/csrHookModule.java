import com.alibaba.jvm.sandbox.api.Information;
import com.alibaba.jvm.sandbox.api.Module;
import com.alibaba.jvm.sandbox.api.ProcessController;
import com.alibaba.jvm.sandbox.api.annotation.Command;
import com.alibaba.jvm.sandbox.api.listener.ext.Advice;
import com.alibaba.jvm.sandbox.api.listener.ext.AdviceListener;
import com.alibaba.jvm.sandbox.api.listener.ext.EventWatchBuilder;
import com.alibaba.jvm.sandbox.api.resource.ModuleEventWatcher;
import com.alibaba.jvm.sandbox.module.debug.ParamSupported;
import org.kohsuke.MetaInfServices;

import javax.annotation.Resource;
import java.util.Map;

@MetaInfServices(Module.class)
@Information(id = "ceshiren", author = "ceshiren.com")
public class csrHookModule extends ParamSupported implements Module {

    @Resource
    private ModuleEventWatcher moduleEventWatcher;

    @Command("csrhook")
    public void csrHook(final Map<String, String> param) {
        final String className = getParameter(param, "class");
        final String methodName = getParameter(param, "method");
        final String hookType = getParameter(param, "type");
        new EventWatchBuilder(moduleEventWatcher)
                .onClass(className)
                .onBehavior(methodName)
                .onWatch(new AdviceListener() {
                    @Override
                    protected void before(Advice advice) throws Throwable {
                        if (hookType.equals("args")) {
                            // 修改函数的传入参数
                            final int argsNum = getParameter(param, "param_num", int.class);
                            final String argsType = getParameter(param, "param_type");
                            if (argsType.equals("int")) {
                                final int argsData = getParameter(param, "param_data", int.class);
                                advice.changeParameter(argsNum, argsData);
                            } else if (argsType.equals("boolean")) {
                                final Boolean argsData = Boolean.getBoolean(getParameter(param, "param_data"));
                                advice.changeParameter(argsNum, argsData);
                            } else {
                                final String argsData = getParameter(param, "param_data");
                                advice.changeParameter(argsNum, argsData);
                            }
                        }
                        if (hookType.equals("direct_return")) {
                            // 进入函数后就直接返回，mock掉函数内部语句和逻辑，将设置的数值作为返回值返回回去
                            final String paramType = getParameter(param, "param_type");
                            if (paramType.equals("int")) {
                                final int returnData = getParameter(param, "param_data", int.class);
                                ProcessController.returnImmediately(returnData);
                            } else if (paramType.equals("boolean")) {
                                final Boolean returnData = Boolean.getBoolean(getParameter(param, "param_data"));
                                ProcessController.returnImmediately(returnData);
                            } else {
                                final String returnData = getParameter(param, "param_data");
                                ProcessController.returnImmediately(returnData);
                            }
                        }
                    }
                });
    }

}