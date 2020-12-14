/**
 * @name Lines of code in files
 * @description The number of lines of code in a file.
 */
import java

// https://github.com/github/codeql/blob/main/java/ql/src/Metrics/Files/FLinesOfCode.ql

from File f, int n
where n = f.getNumberOfLinesOfCode()
select f, n order by n desc
