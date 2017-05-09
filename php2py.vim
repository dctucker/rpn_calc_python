" Can be called via the following shell incantation:
" ex Outbrain.php < php2py.vim

:set ts=4 noexpandtab
" <?php     
%s/<?php//g
" ?>        
%s/?>//g
" public function name($var);          def name(var): \n\t pass
%s/^\(\s*\)public function \(\w*\)\s*(\([^)]*\));$/\1def \2(self, \3):\r\1\tpass\r/g
" static function &name(x,y){}         @classmethod def name(self, x,y): pass
%s/\n\t\w*\s*static function &\?\(\w*\)\s*(\([^)]*\))\(\_s*\){\(\_s*\)}$/\t@classmethod\r\tdef \1(cls, \2): pass \3\4/g
" function &name(x,y){}                def name(self, x,y): pass
%s/function &\?\(\w*\)\s*(\([^)]*\))\(\_s*\){\(\_s*\)}$/def \1(self, \2): pass \3\4/g

" \Exception (_                        Exception (_
%s/\\Exception\([ (]\)/Exception\1/g
" __METHOD__                           ''
%s/__METHOD__/''/g
"# %s/interface \(.*\)$/class \1/g

" class name \_ implements \_ ... {    class name \_ """ implements \_ ... """
%s/\(class\s*[A-Za-z ]*\s*\)\_\s*implements\(\_[^{]*\){/\1\r\timplements = [\2]/g
" try                                  try:
%s/try$/try:/g
" catch ( \Exception\Exc $e ){}        except Exception\Exc as e: pass
%s/catch\s*(\s*\\*\([A-Za-z\\]*\)\s*\$\([A-Za-z]*\)\s*){}$/except \1 as \2: pass/g
" catch ( \Exception\Exc $e )          except Exception\Exc as e:
%s/catch\s*(\s*\\*\([A-Za-z\\]*\)\s*\$\([A-Za-z]*\)\s*)$/except \1 as \2:/g
" throw                                raise
%s/throw/raise/g
" (abcde, Abcde $var234, abcde)        (abcde, var234, abcde)
%s/(\([^()]*[, ]\)[A-Z][A-Za-z]*\(\s\+\)\$\(\w*\)\([^()]*\))/(\1\2\3\4)/g
" true                                 True
%s/\([^"']\)true\([^"']\)/\1True\2/g
" false                                False
%s/\([^"']\)false\([^"']\)/\1False\2/g
" do \n { ... }                        condition = True \n while condition:
%s/\(\t*\)\<do\>\n\?/\1condition=True\r\1while condition:/g
" while ( a > b );                     condition = a > b
%s/while\s*\(.*\);/\tcondition = \1/g
"# %s/static \$\([A-Za-z_]*\);$/\1 = None/g
%s/^\s*\zswhile\s*(\([^;]*\))\ze\n\s*{/while \1:/g

" protected static $var =              var =
%s/\(public\|private\|protected\|static\)\( static\)\? \$\([A-Za-z_]*\) = /\3 = /g
"# protected static $var = 'value';     var = 'value'
"#%s/\(public\|private\|protected\|static\)\( static\)\? \$\([A-Za-z_]*\) = \([^;]*\);$/\3 = \4/g
" private static $var;                 var = None
%s/\(public\|private\|protected\|static\)\( static\)\? \$\([A-Za-z_]*\);$/\$\3 = None/g
" ! $var                               not $var
%s/\([ (]\)!\([ ($a-z]\)/\1 not \2/g
" a !== false                          $a is not False
%s/!== False/is not False/g
" a !== b                              $a != $b
%s/!==/!=/g
" $a->$b[] = $c                        getattr(a,b).push(c)
%s/\$\([^- ]*\)->\$\([^ ]*\)\[\] = \([^;]*\)/getattr(\1,\2).append(\3)/g
" $something[] = $b                    $something.append(b)
%s/\[\] = \(\_[^;]*\);$/.append(\1)/g
" array_merge($a, $b)                  $b.update($a)
%s/\<array_merge(\(\_[^)]\+\),\(\_[^)]\+\))/\2.update(\1)/
"# array_search($a, $b)                 [ k for k,v in \2.iteritems() if v == \1 ][0]
"# %s/\<array_search(\(\_[^)]\+\),\(\_[^)]\+\))/[ k for k,v in \2.iteritems() if v == \1][0]/
" ; <EOL>                              <EOL>
%s/;$//g
" $a && $b                             $a and $b
%s/ && / and /g
" $a || $b                             $a or $b
%s/ || / or /g
" &$var                                $var
%s/&\$/\$/g
" $map                                 $map_
%s/\$map/\$map_/g
" foreach( $a as $i => $value )        for i,value in enumerate(a):
%s/foreach(\s*\$\([^ ]*\) as \$\([ij]*\)\s*=>\s*\([^ ]*\)\s*)/for \2,\3 in enumerate(\1):/g
" foreach( $a as $k => $v )            for k,v in a.items():
%s/foreach(\s*\$\([^ ]*\) as \$\([^ ]*\)\s*=>\s*\([^ ]*\)\s*)/for \2,\3 in \1.items():/g
" foreach( $a as $b )                  for b in a:
%s/foreach(\s*\$\([^ ]*\) as \$\([^ ]*\)\s*)/for \2 in \1:/g
" foreach( [ ... ] as $b )              for b in [...]:
%s/foreach(\s*\(\[[^]]\+\]\) as \$\([^)]*\))/for \2 in \1:/g
"  ..."lorem $ipsum ...                ..."lorem" . $ipsum . " ...
%s/^\([^"]*["][^"]*\)\$\([A-Za-z_]\+\)/\1" . \$\2 . "/g
" dot quote quote                      (remove trailing concat '')
%s/ . ""//g
" ->class                              ->class_name
%s/->\<class\>/->class_name/g
" ->items                              ['items']
%s/->\<items\>/['items']/g
" $class =                             class_name =
%s/\$class = /\$class_name = /g
" $class(                              $class_name(
%s/\$class\([ (]\)/\$class_name\1/g
" unset( $a->$b )                      delattr($a,b)
%s/unset(\([^-)]*\)->\$\([^)]*\))/delattr(\1, \2)/g
" unset( $a->{"b"} )                   delattr($a,"b")
%s/unset(\([^-)]*\)->{\([^}]*\)})/delattr(\1, \2)/g
" unset( $a[$b] )                      del $a[$b]
%s/unset(\([^[]*\)\[\([^\]]*\)\])/del \1[\2]/g
" unset( $a->b )                       delattr($a,'b')
%s/unset(\([^)]*\)->\([^$-> ]*\)\s*)/unset(\1, '\2')/g
" isset( $a[$b] )                      $b in $a
%s/isset(\s*\([^)]\+\)\[\([^]]*\)\]\s*)/(\2 in \1)/g
" isset( $this->abcde )                (self.abcde is not None)
%s/isset(\s*\$this->\([^) ]*\)\s*)/(self.\1 is not None)/g
" isset( $a->$b )                      ( b in $a )
%s/isset(\s*\([^-)]*\)->\$\([^) ]*\)\s*)/(\2 in \1)/g
" isset( $a->{"abcde"} )               ('abcde' in $a)
%s/isset(\s*\([^-)]*\)->\([^) ]*\)\s*)/('\2' in \1)/g
" $a->$b = $c                          setattr(a,b,c)
%s/\$\([^- ]*\)->\$\([^ ]*\) = \([^;]*\)/setattr(\1,\2,\3)/g
" $a->$b                               getattr(a,b)
%s/\$\([^- ]*\)->\$\([^ ]*\)/getattr(\1,\2)/g
" in_array( $a, $b )                   ( b in a )
%s/in_array(\([^,)]*\),\([^)]*\))/(\1 in \2)/g
" is_array( $a )                       isinstance( $a, (list,tuple,dict))
%s/is_array(\([^)]*\))/isinstance(\1, (list,tuple,dict))/g
" is_object( $a )                      isinstance( $a, (dict,object))
%s/is_object(\([^)]*\))/isinstance(\1, (dict, types.TypeType, types.ClassType))/g
" is_null( $a )                        $a is None
%s/is_null(\([^)]*\))/\1 is None/g
" $                                    
%s/\$//g
"#" for( $i=0 ; $i < 5; $i++ )           for i in range( 0, 5 ):
"#%s/for\s*(\(\w*\)\s*=\s*\([^;]*\);\s*\(\w*\)\s*[!<>=]*\s*\([^;]*\);\([^;]*\))/for \1 in range( \2, \4 ):/g
" for( $i=0 ; $i < 5; $i++ )           for i in range( 0, 5 ):
%s/^\n\(\s*\)for\s*(\(\w*\)\s*=\s*\([^;]*\);\s*\(\w*\s*[!<>=]*\s*[^;]*\);\([^;]*\))\_s*{$/\1\2 = \3\r\1while \4:\r\1\t\5/g
" x .= y                               x += y
%s/\.=/+=/g
" list( a, b ) = ...                   ( a, b ) = ...
%s/list\(/\(/g
" a => b                               a:b
%s/\s*=>/:/g
"  .                                    +     (string concatenation)
%s/ \. / + /g
" ->                                   .      (object indirection)
%s/->/./g
" if( condition )                      if( condition ):
%s/if(\(.*\))$/if \1:/g
" else \n                              else:
%s/else$/else:/g
" \n \t \t }                           \n
%s/\n\t*}/\r/g
" elseif                               elif
%s/elseif/elif/g
" else{                                else:
%s/else{/else:/g
" echo                                 print
%s/echo/print/
" null                                 None
%s/NULL/None/ig
" i++                                  i+=1
%s/++/+=1/g
"# x instanceof y                       isinstance(x,y)
"#%s/\([^ ]*\) instanceof \([^ ]*\)/isinstance(\1,\2)/g
" x instanceof y                       y in [ t.__name__ for t in x.mro() ]
%s/\([^ ]*\) instanceof \([^ ]*\)/\2 in [ t.__name__ for t in \1.__class__.mro() ]/g
" ucfirst('whatever')                  'whatever'.capitalize()
%s/ucfirst(\(.*\))/\1.capitalize()/g
" is_numeric( x )                      x.isdigit()
%s/is_numeric\(([^ ]*)\)/$1.isdigit()/g
" strlen                               len
%s/\<strlen\>/len/gg
" count                                len
%s/[^"']\zs\<count\>\ze[^"']/len/gg
"# empty( x )                           len(x) is 0
"# %s/empty(\([^)]*\))/len(\1) == 0/g
" empty( x[y] )                        empty(x,y)
%s/empty(\s*\([^[]*\)\[\([^]]*\)\]\s*)/empty(\1,\2)/g
"    { \n                              \n
%s/\s*{\n/\r/
" protected                            
%s/protected //g
" private                              
%s/private //g
" public                               
%s/public//g
"     static function &name(x,y)       @classmethod \n def name(cls, x,y):
%s/^\(\s*\)static function &\?\([^(]\+\)(\([^)]*\))\n\(\s*\)/\1@classmethod\r\1def \2(cls, \3):/g
" function &name(x,y)                  def name(self, x,y):
%s/function &\?\(\w*\)\s*(\([^)]*\))/def \1(self, \2):/g

"# %s/protected def \([^)]*)\)/def _\1:/g
"# %s/private def \([^)]*)\)/def __\1:/g
let self=expand('%:t:r')
" parent::                             super(Class, self).
%s/parent::/\='super('.self.', self).'/g
"# static::                             Class.
"#%s/static::/\=''.self.'.'/g
" static::                             self.__class__.
%s/static::/self.__class__./g
"     x = self::var                        x = var    (class level)
%s/^\(\t\w\+\) = self::\(.*\)$/\1 = \2/g
" self::                               Class.
%s/self::/\=''.self.'.'/g
" this                                 self
%s/this/self/g
" (self, )                             (self)             (remove trailing comma)
%s/(self, )/(self)/g
" (cls, )                              (cls)              (remove trailing comma)
%s/(cls, )/(cls)/g
" ::class                              .__class__
%s/::class\>/.__name__/g
" ::                                   .
%s/::/./g
" for ( ... )                          for ... :
%s/for\(\s*([^)]\))/for\1:/g
" use ...                              import ...
%s/^use \(.*\)$/import \1/g
"# %s/\(^[^']*'[^']*\)\\\\\([^']*'\)/\1\\\2/g

" \                                    .                  (namespace path separator)
%s/\\\([^nr\\]\)/.\1/g
" \.                                   .                  (remove leading backslash)
%s/\\\././g
" namespace ...                        # namespace ...
%s/^\(namespace .*\)$/#\1/g
" interface Name {}                    class ... \n\t pass
%s/^interface \([^)]*\) {}$/class \1\r\tpass/g
" interface Name                       class Name
%s/^interface \([^)]*\)$/class \1/g
" abstract class ...                   class ...(object):
%s/^abstract class \(.*\)/class \1(object):/g
" class Name extends ..Parent {}       from Parent import Parent \n class Name(Parent): \n\t pass
%s/^\nclass \([^)]*\) extends \.*\([^)]*\) {}$/from \2 import \2\rclass \1(\2):\r\tpass\r/g
" class Name extends ..Parent          from Parent import Parent \n class Name(Parent):
%s/^\nclass \([^)]*\) extends \.*\([^)]*\)$/from \2 import \2\rclass \1(\2):/g
" class Name                           class Name:
%s/^class \([^)]*\)$/class \1:/g
"     abstract def ...                     def ... \n pass
%s/\(\t*\)abstract\s\+\(def .*\)$/\1\2\r\1\tpass/g
" new static( x, y )                   Name( x, y )
%s/\(new static\)\ze\(([^)]*)\)$/\=self/g
" new ..Name( x, y )                   Name( x, y )
%s/new \.*\(\w*\)\(([^)]*)\)$/\1\2/g
" new ..Name                           Name
%s/new \.*\(\w*\)$/\1/g
" = new Name                           = Name
%s/= new \(\w*\)/= \1/g
" raise new                            raise
%s/raise new /raise /g
" class Name extends Parent            class Name(Parent)
%s/^class .*\zs extends \(.\+\):/(\1):/g
" /**                                  """
%s/\/\*\**/"""/g
" **/                                  """
%s/\**\*\//"""/g
" \t *                                 \t            (make comments pretty?)
%s/\t \* /\t/g
" \t                                   \t
%s/\t /\t/g
"  abc[ def                            abc{ def
%s/^\(\s*[^#]\+\)\[\([^_]\)/\1{\2/g
" [                                    {             (at end of line)
%s/\[$/{/g
" def ]                                def }
%s/^\(\s*[^#]\+[^_]\)\]/\1}/g
" abc{"def"}                           abc["def"]
%s/\([^.]\){\(['"][^'"]*['"]\)}/\1\[\2\]/g
" {123}                                [123]
%s/{\([0-9]\+\)}/[\1]/g
"     //                                   #
%s/\(\s\)\/\//\1#/g
" //                                   #
%s/\/\/\(\s\)/#\1/g

" = foo() #py= bar()                   = bar() #php= foo()
%s/= \([^#]\+\)#py= \(.*\)$/= \2 #php= \1/g
"     #py foo()                            foo()
%s/^\(\s*\)#py \(.*\)$/\1\2/g
" : #py ...                            : ...
%s/: #py \(.*\)$/: \1/g
"     code #pyno                           #php code
%s/\(^\s*\)\([^ ]\+.* \)#pyno$/\1#php \2/g
"     #pyno \_ ... \n     #pyon        """php \n ... \n php"""
%s/^\(\s*\)#pyno\n\(\_[^#]*\)\n\s*#pyon$/\1"""php\r\2\r\1php"""/g

" (object) something                   something
%s/(object)\([^:]\)/\1/g
" (array)                              
%s/(array)//g
" (bool) something                     boolean(something)
%s/(bool)\s*\([^ ]*\)/bool(\1)/g
" (boolean) something                  boolean(something)
%s/(boolean)\s*\([^ ]*\)/bool(\1)/g
" array()                              list([])
%s/\<array\>()/list()/g
" array                                
%s/\<array\>//g
" const                                
%s/const //g
" base64_encode                        base64.b64encode
%s/base64_encode/base64.b64encode/g
" __construct                          __init__
%s/__construct/__init__/g
"# a.{"b"}                             getattr(a,b)
"# %s/\(\w*\)\.{\(['"][^'"]*['"]\)}/getattr(\1,\2)/g
" name.{"string"}                      name["string"]
%s/\(\w*\)\.{\(['"][^'"]*['"]\)}/\1[\2]/g
" unset(getattr(a,b))                  delattr(a,b)
%s/unset(getattr(\([^,]*\),\([^)]*\)))/delattr(\1,\2)/g
"# unset(a)                            delete a
"# %s/unset(\([^)]*\))/delete \1/g
" from                                 fro            (variable name)
%s/\([^"']\)from\([^'"]\)/\1fro\2/g
" from                                 fro            (variable name)
%s/\([^"']\)from$/\1fro/g
" a.{b}                                getattr(a,b)
%s/\([^ ]*\)\.{\(.*\)}\((.*)\)/getattr(\1, \2)\3/g
" a ?? b                               a or b
%s/\([^?]\+\) ?? \([^?]\+\)$/\1 or \2/g
" a ?: b                               a or b
%s/\(^\s*\)\([^=]*\)=\([^?]*\) ?: \(.*\)$/\1\2=\3 or \4/g
" var = a ? b : c                      var = b if a else c
%s/\(^\s*\)\([^=]*\)=\([^?]*\) ? \([^:]\+\):\(.*\)$/\1\2=\4 if \3 else \5/g
" a ?: b                               a or b
%s/\([^:=>?]\+\) ?: \([^,;]\+\)/\1 or \2/g
" a ? b : c                            b if a else c
%s/\([^:=>?]\+\) ? \([^:]\+\) : \([^,;]\+\)/\2 if \1 else \3/g
" if case:                             if case: pass
%s/\(\s*\)\(if case[^:]*:\)\(\n\1\w\)/\1\2 pass\3/g

"# """ \_ comments """ \n def ...      def \n \t """ comments """
"# %s/\("""\_[^"""]*"""\)\(\n\s*def .*\)/\2\r\t\1/g
"# remove extra spaces
"# %s/  / /g

" #pyno \n \_ ... \n #pyon             """php \n ... \n php"""       (same as above)
%s/^\(\s*\)#pyno\n\(\_[^#]*\)\n\s*#pyon$/\1"""php\r\2\r\1php"""/g

" case 'x': \n case 'y':               if case('x'): pass \n if case 'y':
%s/case \([^:]*\):\ze\n\s*\(case \|default:\)/if case(\1): pass/g
" case 'x':                            if case('x'):
%s/case \([^:]*\):/if case(\1):/g
" default:                             if case():
%s/default:/if case():/g
" switch ( var )                       for case in switch( var )
%s/switch\s*(\([^)]*\))/for case in switch(\1):/g

"# if case ...                       (incomplete)
"# %s/\(\s*\)if case\([^:]*\):\n\1[^\s]/
"# %s/^\(\s*\)case \([^:]*\):/\1if case == \2:\r\1\tdefault = False;/g
"# %s/default:/if default:/g
"# %s/switch\s*(\([^)]*\))/default = True; for case in (\1):/g


"#  array_map(   function(    $obj         )   {   return ['id'=>$obj]; }, $data['block_publishers_array'] );
"# %s/array_map(\s*function(\s*\([^ ]*\)\s*)\s*{\s*return \[\([^=]*\)=>\([^]]*\)\];\s*}\s*,\s*\([^)]*\))/[ {\2:\3} for \1 in \4 ]/g
"# %s/array_map(\s*function(\s*\([^ ]*\)\s*)\s*{\s*return \([^;]*\);\s*}\s*,\s*\([^)]*\))/[ \2 for \1 in \3 ]/g


" {this = that}                        {this:that}
%s/{\_s*\zs\(\w\+\)\s*=\s*\(.*\)\ze\_s*}/'\1':\2/g
" array_map(function(o){ return q; }, var);        [ q for o in var ]
%s/array_map\s*(\s*function\s*(\s*\([^)]*\)\s*)\s*{\s*return\s*\([^;]*\);\s*}\s*,\s*\([^)]*\)\s*)/[ \2 for \1 in \3 ]/g
" array_key_exists(a,b)                 b in a
%s/\<array_key_exists\>(\([^,]*\),\([^)]*\))/\1 in \2/g

" %s/^\(\s*\)ret{\(vendor_key\)} = \(.*\)$/\1ret[\2] = \3/g
" {words}                              [words]
%s/{\(\w\+\)}/[\1]/g
" ['id':obj]                           {'id':obj}
%s/\(\[\)\([^{[]\{-\}:[^]}]\{-\}\)\(\]\)/{\2}/g

" {'a','b'}                            ['a','b']
%s/\%({\)\([^:[{]\{-\},[^:}\]]\{-\}\)\%(}\)/\[\1\]/g

%s/\.\.\.\([^,)]\+\)/*\1/g

" Exception e                          e
%s/Exception e/e/g
" trim(var)                            var.strip()
%s/\<trim\>(\(.\+\))/\1.strip()/g
" str_replace(a,b,c)                   c.replace(a,b)
%s/str_replace(\([^,]*\),\([^,]*\),\([^)]*\))/\3.replace(\1,\2)/g
" ucwords(var)                         ' '.join([s[0].upper() + s[1:] for s in var.split(' ')])
%s/ucwords(\([^)]*\))/' '.join([s[0].upper() + s[1:] for s in \1.split(' ')])/g
" strtolower(var)                      var.lower()
%s/\<strtolower\>(\([^)]\+\))/\1.lower()/g
" strtoupper(var)                      var.upper()
%s/\<strtoupper\>(\([^)]\+\))/\1.upper()/g
" time()                               int(time.time())
%s/time()/int(time.time())/g
" intval( a )                          int( a )
%s/intval(\([^)]*\))/int(\1)/g
" microtime(true)                      time.time()
%s/microtime([Tt]rue)/time.time()/g
" iterator_to_array(var)               list(var)
%s/\<iterator_to_array\>(\(.*\))/list(\1)/g
" class_exists                         
%s/class_exists//g
" import Carbon.Carbon                 
%s/import Carbon\.Carbon//g
"#" import GuzzleAnything                import requests
"#%s/import Guzzle.*$/import requests/g
" import GuzzleAnything                  
%s/import Guzzle.*$//g
"# import dctucker.APIs.Something          import Something
"# %s/import dctucker\.APIs\.\(.*\)$/import \1/g
" use dctucker\Tests\UnitTestBase          from tests.UnitTestBase import UnitTestBase
%s/^import Tests\.\(.*\)$/from tests.\1 import \1/g
" __NAMESPACE__                        'dctucker'
%s/__NAMESPACE__/'dctucker'/g
" from Exception import Exception      
%s/from Exception import Exception//g
" import Exception
%s/^import Exception$//g
" e.hasResponse()                      e.response is not None
%s/e.hasResponse()/e.response is not None/g
" e.getResponse().getStatusCode()      e.response.status_code
%s/e.getResponse().getStatusCode()/e.response.status_code/g
"# import This.That                    from This.That import That
"# %s/^import \(.*\)\.\(.*\)$/from \1.\2 import \2/g
" %s/^import \(dctucker\..\{-\}\)\([^.]\+\)$/from \1\2 import \2/g
" import dctucker.Foo.Bar as Baz           from dctucker.Foo.Bar import Bar as Baz
%s/^import \(dctucker\..\{-\}\)\([^. ]\+\) as \([^ ]\+\)$/from \1\2 import \2 as \3/g
" import dctucker.Foo.Bar                  from dctucker.Foo.Bar import Bar
%s/^import \(dctucker\..\{-\}\)\([^. ]\+\)$/from \1\2 import \2/g
" def setUpBeforeClass                 def setUpClass
%s/def setUpBeforeClass/def setUpClass/g
" det __toString(self):                def __str__(self):
%s/def __toString(self):/def __str__(self):/g

" @classmethod ... self.__class__      @classmethod ... cls
%s/^\t@classmethod\n\tdef \w\+(cls,[^)]*):\%(\n\_^\t\t.*\)\{-1,\}\zs\(self.__class__\)/cls/g
%s/^\t@classmethod\n\tdef \w\+([^)]\+):\n\%(\_^\t\t.\_$\)\{-\}\t\t.*\zs\(self.__class__\)/cls/g

"# comment @expectedException comment   comment comment @expected_exception
"#%s/^\t\zs@expectedException\(.*\)$\n\t"""\ze\n\tdef/"""\r\t@expect_exception(\1)/g

" fluent_a() \n .fluent_b()            fluent_a() \ \n .fluent_b()
%s/\n\(\t*\..*\)$/ \\\r\1/g

" { \_... ]                               [ \_... ]
%s/\({\)\(\_[^:[}]\{-\}\)\(\]\)/[\2]/g
" { \_... ]                               { \_... }
%s/\({\)\(\_[^[}]\{-\}\)\(\]\)/{\2}/g

:execute "w! ".substitute(expand('%:r'),"..\/rpn_calc\/","..\/rpn_calc_python\/","g").'.py'
:q
