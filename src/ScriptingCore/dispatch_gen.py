# ############################################################
# Original Author: Georg Fritzsche
#
# Created:    November 6, 2009
# License:    Eclipse Public License - Version 1.0
#            http://www.eclipse.org/legal/epl-v10.html
#
# Copyright 2009 Georg Fritzsche, Firebreath development team
# ############################################################

#!/usr/bin/python

import time
from datetime import date

def tern(a,b,c):
	i = 0
	if(a): i = 1
	return (b,c)[i]

# ######################################

max_args = 10
tab = "\t"
endl = "\n"
headerFileName          = "MethodConverter.h"
includeGuardName        = "METHOD_CONVERTER_H"
methodWrapStructName    = "method_wrapper"
makeWrapperFunctionName = "make_method"
callMethodFunctorName   = "FB::CallMethodFunctor"

indent = 0;
def ind_in():
	global indent
	indent += 1
def ind_out():
	global indent
	indent -= 1
def ind():
	return tab*indent

# ######################################
	
f = open(headerFileName, "w")

def wl(s):
	f.write(ind()+s+endl)

# legal

wl("/**********************************************************\\")
wl("Original Author: Georg Fritzsche")
wl("Generated on: " + date.today().isoformat())
wl("License:      Eclipse Public License - Version 1.0")
wl("              http://www.eclipse.org/legal/epl-v10.html")
wl("")
wl("Copyright 2009 Georg Fritzsche, Firebreath development team")
wl("\\**********************************************************/")
wl("")
	
# start
	
wl("")
wl("#if !defined("+includeGuardName+")")
wl("#define "+includeGuardName)
wl("")
wl("#if defined(_MSC_VER)")
wl("#  pragma once")
wl("#endif")
wl("")

# includes

wl("#include <boost/function.hpp>")
wl("#include <boost/bind.hpp>")
wl("#include \"ConverterUtils.h\"")
wl("")

# prologue

wl("namespace FB")
wl("{")
ind_in()

# wrapper

wl("namespace detail { namespace methods")
wl("{")
ind_in()

for i in range(max_args+1):
	s = "template<class C"
	for i2 in range(i): 
		s += ", typename T"+str(i2)
	wl(s + ", typename F>")
	wl("struct "+methodWrapStructName+str(i)+" {")
	ind_in()
	wl("typedef FB::variant result_type;")
	wl("F f;")
	wl(methodWrapStructName+str(i)+"(F f) : f(f) {}")
	wl("FB::variant operator()(C* instance, const FB::VariantList& in)")
	wl("{")
	ind_in()
	if i<1:
		wl("if(in.size() != 0)")
	else:
		wl("if(!FB::detail::methods::checkArgumentCount<typename FB::detail::plain_type<T"+str(i-1)+">::type>(in, "+str(i)+"))") 
	wl(tab+"throw FB::invalid_arguments(\"Invalid Argument Count\");")
	wl("FB::VariantList::const_iterator it = in.begin();")
	s = "return (instance->*f)(";
#	if i>0:
#		s+="in[0].convert_cast<typename FB::detail::plain_type<T0>::type>()"
#	for i2 in range(1,i):
#		s+= ", in["+str(i2)+"].convert_cast<typename FB::detail::plain_type<T"+str(i2)+">::type>()"
	if i<1:
		wl(s+");")
	else:
		wl(s)
		ind_in()
		s = "FB::convertArgument<typename FB::detail::plain_type<T0>::type>(in[0], 1)"
		if i>1:
			for i2 in range(1,i-1):
				wl(s+",")
				s = "FB::convertArgument<typename FB::detail::plain_type<T"+str(i2)+">::type>(in["+str(i2)+"], "+str(i2+1)+")"
			wl(s+",")
		wl("FB::detail::methods::convertLastArgument<typename FB::detail::plain_type<T"+str(i-1)+">::type>(in, "+str(i)+"));")
		ind_out()
	ind_out()
	wl("}")
	ind_out()
	wl("};")
	
ind_out()
wl("} } // namespace detail::methods")
wl("")
	
# make_wrapper

for i in range(max_args+1):
	typenames = ""
	if i>0:
		typenames += "typename T0"
		for i2 in range(1,i):
			typenames += ", typename T"+str(i2)
	typenames_app = ""
	if i>0:
		typenames_app = ", "+typenames
	types = ""
	if i>0:
		types += "T0"
		for i2 in range(1,i):
			types += ", T"+str(i2)
	print " * "+types
	types_app = ""
	if i>0: 
		types_app = ", "+types
	
	wl("template<class C, typename R"+typenames_app+">")
	wl("inline "+callMethodFunctorName)
	wl(makeWrapperFunctionName+"(C* instance, R (C::*function)("+types+"))")
	wl("{")
	ind_in()
	wl("return boost::bind(FB::detail::methods::"+methodWrapStructName+str(i)+"<C"+types_app+", R (C::*)("+types+")>(function), instance, _1);")
	ind_out()
	wl("}")
	wl("")

# epilogue

ind_out()
wl("} // namespace FB")
wl("")

wl("#endif //"+includeGuardName)
wl("")

f.close()
