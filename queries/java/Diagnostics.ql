import java

/**
 * Holds if file `f` is relevant for error diagnostics reporting.
 */
predicate relevantFile(File file) {
  file.getExtension() = "java" and
  not file.getStem() = "package-info" and
  not file.getStem() = "module-info"
}
/**
 * Holds if extraction of source file `f` failed.
 */
predicate failed(File f) {
  relevantFile(f) and
  not exists(Location loc | diagnostics(_, _, _, _, _, loc) and f = loc.getFile()) and
  not exists(@compilation c, int n |
    compilation_compiling_files(c, n, f) and compilation_time(c, n, _, _)
  )
}
from File file, int severity
where
  severity = max(int s |
      exists(Location loc | file = loc.getFile() and diagnostics(_, s, _, _, _, loc))
      or
      failed(file) and
      s = 9
    ) and
  severity in [4 .. 9]
select file.getRelativePath(), severity order by severity desc
