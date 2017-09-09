# Code copied from jaycode's answer @ https://stackoverflow.com/questions/27934885
# Code has been modified from the original
# This is a cell to hide code snippets from displaying
# This must be at first cell!
from IPython.display import HTML
opacity = 1
htmlscript_for_hiding_cells='''<script>
code_show=true; 
function code_toggle() {{
  if (code_show) {{
    $('div.input').each(
        function(id) {{
          el = $(this).find('.cm-comment:first');
          if (el.text().replace(/\s+/g,'').toLowerCase() == '#hide') {{
            $(this).hide();
            $("#BrrrButton").val("Show Hidden Cells")
          }}
        }}
    );
    $('div.output_prompt').css('opacity', 0);
  }} 
  else {{
    $('div.input').each(
        function(id) {{
          $(this).show();
          $("#BrrrButton").val("Hide Tagged Cells")
        }}
    );
    $('div.output_prompt').css('opacity', 1);
  }}
  code_show = !code_show
}} 
$( document ).ready(code_toggle);
</script>
<form action="javascript:code_toggle()"><input id="BrrrButton" style="opacity:{opacity}" type="submit" value="Hide Tagged Cells"></form>'''

