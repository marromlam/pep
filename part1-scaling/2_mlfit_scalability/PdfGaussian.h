
#ifndef PDFGAUSSIAN
#define PDFGAUSSIAN

#include "AbsPdf.h"
#include "Variable.h"

#define RooGaussian PdfGaussian

class PdfGaussian : public AbsPdf {
public:
  PdfGaussian(const Char_t* name, const Char_t* title, Variable &x,
	      Variable &mu, Variable &sigma);
  virtual ~PdfGaussian() { }

  virtual void GetParameters(List<Variable>& parameters) { parameters.AddElement(*m_mu); parameters.AddElement(*m_sigma); }
  
 protected:
  virtual Double_t evaluate() const;
  virtual Double_t integral() const;
  
  virtual Bool_t evaluateSIMD(const UInt_t& iPartialStart, const UInt_t& nPartialEvents,
			      const Double_t invIntegral);

 private:
  inline Double_t evaluateLocal(const Double_t x, const Double_t mu,
				const Double_t sigma) const {
    return TMath::Exp(-((Double_t)0.5)*TMath::Power((x-mu)/sigma,2));
  }
  
 private:
  Variable *m_x;
  Variable *m_mu;
  Variable *m_sigma;

};

#endif
