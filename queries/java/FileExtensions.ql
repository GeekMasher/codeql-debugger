import java

from File f, string ext
where ext = f.getExtension()
select ext as extension, count(File file | ext = file.getExtension()) as frequency order by
    frequency desc
