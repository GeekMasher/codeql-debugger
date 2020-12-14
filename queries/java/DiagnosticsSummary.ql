/**
 * @description For each diagnostic severity between 0 and 9,
 *              the number of source files corresponding to that severity.
 *              A severity of 4 or above indicates an extraction error.
 */
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
/**
 * Gets the highest diagnostic severity for file `f`.
 */
int maxSeverity(File file) {
  result = max(int s |
      exists(Location loc | file = loc.getFile() and diagnostics(_, s, _, _, _, loc))
      or
      failed(file) and
      s = 9
    ) and
  result in [1 .. 9]
}
from int severity, int numFiles
where
  numFiles = strictcount(File file | severity = maxSeverity(file)) and
  severity in [1 .. 9]
  or
  numFiles = strictcount(File file | relevantFile(file) and not exists(maxSeverity(file))) and
  severity = 0
select severity, numFiles order by severity desc