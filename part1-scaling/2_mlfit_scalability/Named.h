
#ifndef NAMED
#define NAMED

#include <string>

// Basic definitions by ROOT
#define kTRUE true
#define kFALSE false

class Named {
 public:

  Named(const char* name, const char* title);
  virtual ~Named() { }

  inline const char* GetName() const { return m_name.c_str(); }
  
 private:
  std::string m_name;
  std::string m_title;

};

#endif
