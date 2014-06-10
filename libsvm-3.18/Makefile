CXX? = g++
CFLAGS = -Wall -Wconversion -O3 -fPIC
SHVER = 2
OS = $(shell uname)

all: svm-train svm-predict svm-scale

lib: svm.o
	if [ "$(OS)" = "Darwin" ]; then \
		SHARED_LIB_FLAG="-dynamiclib -Wl,-install_name,libsvm.so.$(SHVER)"; \
	else \
		SHARED_LIB_FLAG="-shared -Wl,-soname,libsvm.so.$(SHVER)"; \
	fi; \
	$(CXX) $${SHARED_LIB_FLAG} svm.o -o libsvm.so.$(SHVER)

svm-predict: svm-predict.c svm.o eval.o
	$(CXX) $(CFLAGS) svm-predict.c svm.o eval.o -o svm-predict -lm
svm-train: svm-train.c svm.o eval.o
	$(CXX) $(CFLAGS) svm-train.c svm.o eval.o -o svm-train -lm
svm-scale: svm-scale.c
	$(CXX) $(CFLAGS) svm-scale.c -o svm-scale
svm.o: svm.cpp svm.h
	$(CXX) $(CFLAGS) -c svm.cpp
eval.o: eval.cpp eval.h svm.h
	$(CXX) $(CFLAGS) -c eval.cpp -o eval.o

clean:
	rm -f *~ svm.o eval.o svm-train svm-predict svm-scale libsvm.so.$(SHVER)
