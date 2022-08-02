#!/usr/bin/python

import os, sys;
from pathlib import Path

def cmp_lines(a, b):
    return a[0] > b[0]


def main():
    if len(sys.argv) < 2:
        print("""Usage: 
            ./refmeter.py path [sortColumnNumber]
            example:
            ./refmeter.py
            ./refmeter.py . 1  <- sort by first column, which is line count, default is 5
            columns:
            1 - line count per file
            2 - code blocks count ( what is inside {} )
            3 - parameter blocks count (what is inside () )
            4 - 'case' operator per file ( as for it indicates code block, but does not wrapped in {} )
            5 - max nest level per file (   {} is 1, { {} } is 2  ) <- default
                if() { // nest level 1
                    if() { // nest level 2
                            if() { // nest level 3
                            }
                        }
                    }
            """);
        return;
    
    path=sys.argv[1];
    sortColumnNumber=5
    if( len(sys.argv) == 3 ):
        try:
            sortColumnNumber=int(sys.argv[2]);
        except ValueError:
            print("Warning: sort column number "+sys.argv[2]+" is not integer, using default value 5")
    filetypesString = ".abap .asc .ash .ampl .mod .g4 .apl .dyalog .asp .asax .ascx .ashx .asmx .aspx .axd .dats .hats .sats .as .adb .ada .ads .agda .als .cls .applescript .scpt .arc .ino .aj .asm .a51 .inc .nasm .aug .ahk .ahkl .au3 .awk .auk .gawk .mawk .nawk .bat .cmd .befunge .bison .bb .bb .decls .bmx .bsv .boo .b .bf .brs .bro .c .cats .h .idc .w .cs .cake .cshtml .csx .cpp .c++ .cc .cp .cxx .h .h++ .hh .hpp .hxx .inc .inl .ipp .tcc .tpp .chs .clp .cmake .cmake.in .cob .cbl .ccp .cobol .cpy .capnp .mss .ceylon .chpl .ch .ck .cirru .clw .icl .dcl .click .clj .boot .cl2 .cljc .cljs .cljs.hl .cljscm .cljx .hic .coffee ._coffee .cake .cjsx .cson .iced .cfm .cfml .cfc .lisp .asd .cl .l .lsp .ny .podsl .sexp .cp .cps .cl .coq .v .cr .feature .cu .cuh .cy .pyx .pxd .pxi .d .di .com .dm .d .dart .djs .dylan .dyl .intr .lid .E .ecl .eclxml .ecl .e .ex .exs .elm .el .emacs .emacs.desktop .em .emberscript .erl .es .escript .hrl .xrl .yrl .fs .fsi .fsx .fx .flux .f90 .f .f03 .f08 .f77 .f95 .for .fpp .factor .fy .fancypack .fan .fs .fth .4th .f .for .forth .fr .frt .fs .ftl .fr .gms .g .gap .gd .gi .tst .s .ms .gd .glsl .fp .frag .frg .fs .fsh .fshader .geo .geom .glslv .gshader .shader .vert .vrx .vsh .vshader .gml .kid .ebuild .eclass .glf .gp .gnu .gnuplot .plot .plt .go .golo .gs .gst .gsx .vark .grace .gf .groovy .grt .gtpl .gvy .gsp .hcl .tf .hlsl .fx .fxh .hlsli .hh .php .hb .hs .hsc .hx .hxsl .hy .bf .pro .dlm .ipf .idr .lidr .ni .i7x .iss .io .ik .thy .ijs .flex .jflex .jq .jsx .j .java .jsp .js ._js .bones .es .es6 .frag .gs .jake .jsb .jscad .jsfl .jsm .jss .njs .pac .sjs .ssjs .sublime-build .sublime-commands .sublime-completions .sublime-keymap .sublime-macro .sublime-menu .sublime-mousemap .sublime-project .sublime-settings .sublime-theme .sublime-workspace .sublime_metrics .sublime_session .xsjs .xsjslib .jl .krl .sch .brd .kicad_pcb .kt .ktm .kts .lfe .ll .lol .lsl .lslp .lvproj .lasso .las .lasso8 .lasso9 .ldml .lean .hlean .l .lex .ly .ily .b .m .lagda .litcoffee .lhs .ls ._ls .xm .x .xi .lgt .logtalk .lookml .ls .lua .fcgi .nse .pd_lua .rbxs .wlua .mumps .m .m4 .m4 .ms .mcr .muf .m .mak .d .mk .mkfile .mako .mao .mathematica .cdf .m .ma .mt .nb .nbp .wl .wlt .matlab .m .maxpat .maxhelp .maxproj .mxt .pat .m .moo .metal .minid .druby .duby .mir .mirah .mo .mod .mms .mmk .monkey .moo .moon .myt .ncl .nsi .nsh .n .axs .axi .axs.erb .axi.erb .nlogo .nl .lisp .lsp .nim .nimrod .nit .nix .nu .numpy .numpyw .numsc .ml .eliom .eliomi .ml4 .mli .mll .mly .m .h .mm .j .sj .omgrofl .opa .opal .cl .opencl .p .cls .scad .ox .oxh .oxo .oxygene .oz .pwn .inc .php .aw .ctp .fcgi .inc .php3 .php4 .php5 .phps .phpt .pls .pck .pkb .pks .plb .plsql .sql .sql .pov .inc .pan .psc .parrot .pasm .pir .pas .dfm .dpr .inc .lpr .pp .pl .al .cgi .fcgi .perl .ph .plx .pm .pod .psgi .t .6pl .6pm .nqp .p6 .p6l .p6m .pl .pl6 .pm .pm6 .t .l .pig .pike .pmod .pogo .pony .ps1 .psd1 .psm1 .pde .pl .pro .prolog .yap .spin .pp .pd .pb .pbi .purs .py .bzl .cgi .fcgi .gyp .lmi .pyde .pyp .pyt .pyw .rpy .tac .wsgi .xpy .qml .qbs .pro .pri .r .rd .rsx .rbbas .rbfrm .rbmnu .rbres .rbtbar .rbuistate .rkt .rktd .rktl .scrbl .rl .reb .r .r2 .r3 .rebol .red .reds .cw .rpy .rs .rsh .robot .rg .rb .builder .fcgi .gemspec .god .irbrc .jbuilder .mspec .pluginspec .podspec .rabl .rake .rbuild .rbw .rbx .ru .ruby .thor .watchr .rs .rs.in .sas .smt2 .smt .sqf .hqf .sql .db2 .sage .sagews .sls .scala .sbt .sc .scm .sld .sls .sps .ss .sci .sce .tst .self .sh .bash .bats .cgi .command .fcgi .ksh .sh.in .tmux .tool .zsh .sh-session .shen .sl .smali .st .cs .tpl .sp .inc .sma .nut .stan .ML .fun .sig .sml .do .ado .doh .ihlp .mata .matah .sthlp .sc .scd .swift .sv .svh .vh .txl .tcl .adp .tm .tcsh .csh .t .thrift .t .tu .ts .tsx .upc .uno .uc .ur .urs .vcl .vhdl .vhd .vhf .vhi .vho .vhs .vht .vhw .vala .vapi .v .veo .vim .vb .bas .cls .frm .frx .vba .vbhtml .vbs .volt .webidl .x10 .xc .xsp-config .xsp.metadata .xpl .xproc .xquery .xq .xql .xqm .xqy .xs .xslt .xsl .xojo_code .xojo_menu .xojo_report .xojo_script .xojo_toolbar .xojo_window .xtend .y .yacc .yy .zep .zimpl .zmpl .zpl .ec .eh .fish .mu .nc .ooc .wisp .prg .ch .prw"
    filetypes = filetypesString.split(" ");
    print("Analyzing path: " + path);
    filesCounter = 0;
    linesReport = [];
    linesCounter = 0;
    filenames = [];
    #for filetype in filetypes:
    for filename in Path(path).rglob("*.*"):
        #print( Path(filename).suffix )
        if Path(filename).suffix in filetypes:
            filenames.append(filename)
            
    for filename in filenames:
        filesCounter = filesCounter+1
        print( filename )
        if not os.path.isfile( filename ):
            continue
        with open (filename, "r", errors='replace') as csfile:
            #print( filename )
            lines=csfile.readlines()
            data = ' '.join(lines);
            braceCurrent = 0;
            braceMax = 0;
            for char in data:
                if char == "{":
                    braceCurrent += 1;
                    if braceCurrent > braceMax:
                        braceMax = braceCurrent
                    continue;
                if char == "}":
                    braceCurrent -= 1;
                    
            linesReport.append([filename, 
                                len(lines),
                                data.count('{'),
                                data.count('('),
                                data.count('case'),
                                braceMax
                                ]);
    #print("*.cs files count = " + str(filesCounter) );
    
    linesReport.sort( key = lambda x: x[sortColumnNumber] )
    
    for line in linesReport:
        linesCounter += line[1]
        print( str(line[1]) + "\t" + str(line[2]) + "\t" + str(line[3])+ "\t" + str(line[4])+"\t" + str(line[5])+ "\t" + str(line[0]) )
    print("----------------------------------------")
    print("lines\t{}\t()\tcase\t{} depth")
    
    print("total files count = " + str(filesCounter) );
    print("total lines count = " + str(linesCounter) );
    
if __name__ == "__main__":
    main()