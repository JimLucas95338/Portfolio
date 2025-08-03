# AI Risk Assessment Template for Healthcare Systems

## Assessment Overview

**System Name**: _[AI System/Model Name]_  
**Assessment Date**: _[Date]_  
**Assessor(s)**: _[Name(s) and Role(s)]_ - Include both technical and clinical perspectives  
**Review Period**: _[Assessment validity period]_ - AI changes fast, so don't make this too long  
**Next Review Date**: _[Date]_ - Earlier if anything significant changes  

## System Classification

### Clinical Impact Level
- [ ] **Class I - Low Risk**: Just providing information, doctors make all decisions
- [ ] **Class II - Moderate Risk**: Makes suggestions but doctors always have final say
- [ ] **Class III - High Risk**: Makes decisions on its own or handles life-critical situations

### Regulatory Classification
- [ ] **Non-Medical Device**: Administrative or operational AI
- [ ] **Software as Medical Device (SaMD)**: FDA regulated medical software
- [ ] **AI/ML-Enabled Medical Device**: Hardware with AI components
- [ ] **Clinical Decision Support (CDS)**: AI providing treatment recommendations

### Data Sensitivity Level
- [ ] **Public Data**: De-identified, publicly available datasets
- [ ] **Internal Data**: Institutional data with limited PHI
- [ ] **Protected Health Information (PHI)**: Full HIPAA-covered data
- [ ] **Highly Sensitive**: Genetic, psychiatric, or substance abuse data

## Risk Assessment Matrix

### 1. Patient Safety Risks

#### Clinical Decision Impact
| Risk Factor | Low (1) | Medium (2) | High (3) | Assessment | Mitigation |
|-------------|---------|------------|----------|------------|------------|
| **Diagnostic Accuracy** | >95% sensitivity/specificity | 90-95% accuracy | <90% accuracy | _[Score]_ | _[Plan]_ |
| **False Positive Rate** | <5% | 5-15% | >15% | _[Score]_ | _[Plan]_ |
| **False Negative Rate** | <2% | 2-10% | >10% | _[Score]_ | _[Plan]_ |
| **Clinical Override** | Easy override available | Override with justification | No override capability | _[Score]_ | _[Plan]_ |
| **Failure Mode Impact** | Minimal clinical impact | Moderate care delays | Patient safety risk | _[Score]_ | _[Plan]_ |

#### Patient Population Impact
| Risk Factor | Low (1) | Medium (2) | High (3) | Assessment | Mitigation |
|-------------|---------|------------|----------|------------|------------|
| **Population Size** | <1,000 patients/year | 1,000-10,000 patients | >10,000 patients | _[Score]_ | _[Plan]_ |
| **Vulnerable Populations** | General adult population | Elderly or chronic conditions | Pediatric or critical care | _[Score]_ | _[Plan]_ |
| **Disease Severity** | Non-life threatening | Chronic management | Acute/life-threatening | _[Score]_ | _[Plan]_ |
| **Treatment Urgency** | Routine/preventive | Urgent (hours to days) | Emergency (minutes) | _[Score]_ | _[Plan]_ |

### 2. Bias and Fairness Risks

#### Algorithmic Fairness
| Risk Factor | Low (1) | Medium (2) | High (3) | Assessment | Mitigation |
|-------------|---------|------------|----------|------------|------------|
| **Training Data Diversity** | Representative dataset | Some groups underrepresented | Significant bias in training data | _[Score]_ | _[Plan]_ |
| **Historical Bias** | No known historical bias | Limited historical bias present | Significant historical disparities | _[Score]_ | _[Plan]_ |
| **Performance Equity** | <3% difference across groups | 3-10% performance difference | >10% performance difference | _[Score]_ | _[Plan]_ |
| **Proxy Discrimination** | No protected class proxies | Potential indirect discrimination | Clear proxy discrimination risk | _[Score]_ | _[Plan]_ |

#### Health Equity Impact
| Risk Factor | Low (1) | Medium (2) | High (3) | Assessment | Mitigation |
|-------------|---------|------------|----------|------------|------------|
| **Access Disparities** | No access impact | May affect some populations | Could worsen health disparities | _[Score]_ | _[Plan]_ |
| **Cultural Sensitivity** | Culturally neutral | Some cultural considerations | Significant cultural bias risk | _[Score]_ | _[Plan]_ |
| **Language Barriers** | English-only acceptable | Limited language support needed | Multi-language critical | _[Score]_ | _[Plan]_ |
| **Socioeconomic Impact** | No SES impact | Moderate SES considerations | High SES bias risk | _[Score]_ | _[Plan]_ |

### 3. Privacy and Security Risks

#### Data Protection
| Risk Factor | Low (1) | Medium (2) | High (3) | Assessment | Mitigation |
|-------------|---------|------------|----------|------------|------------|
| **Data Volume** | <1,000 records | 1,000-100,000 records | >100,000 records | _[Score]_ | _[Plan]_ |
| **Data Sensitivity** | De-identified data only | Limited PHI | Full PHI with sensitive data | _[Score]_ | _[Plan]_ |
| **Data Retention** | <1 year retention | 1-7 years retention | >7 years retention | _[Score]_ | _[Plan]_ |
| **Third-Party Access** | No external access | Limited vendor access | Extensive third-party sharing | _[Score]_ | _[Plan]_ |

#### Technical Security
| Risk Factor | Low (1) | Medium (2) | High (3) | Assessment | Mitigation |
|-------------|---------|------------|----------|------------|------------|
| **Model Interpretability** | Fully explainable | Partially interpretable | Black box model | _[Score]_ | _[Plan]_ |
| **Adversarial Robustness** | Robust to attacks | Some vulnerability | High attack risk | _[Score]_ | _[Plan]_ |
| **System Integration** | Standalone system | Limited integration | Extensive system integration | _[Score]_ | _[Plan]_ |
| **Update Mechanism** | Manual controlled updates | Semi-automated updates | Continuous learning/updates | _[Score]_ | _[Plan]_ |

### 4. Regulatory and Compliance Risks

#### Regulatory Requirements
| Risk Factor | Low (1) | Medium (2) | High (3) | Assessment | Mitigation |
|-------------|---------|------------|----------|------------|------------|
| **FDA Requirements** | No FDA oversight | 510(k) clearance needed | PMA approval required | _[Score]_ | _[Plan]_ |
| **HIPAA Compliance** | Minimal PHI exposure | Standard HIPAA compliance | Complex PHI handling | _[Score]_ | _[Plan]_ |
| **State Regulations** | No additional requirements | Some state-specific rules | Multiple state compliance | _[Score]_ | _[Plan]_ |
| **International Standards** | Domestic use only | Limited international use | Global deployment | _[Score]_ | _[Plan]_ |

#### Clinical Governance
| Risk Factor | Low (1) | Medium (2) | High (3) | Assessment | Mitigation |
|-------------|---------|------------|----------|------------|------------|
| **Clinical Validation** | Extensive validation | Moderate validation | Limited validation | _[Score]_ | _[Plan]_ |
| **Provider Training** | Minimal training needed | Standard training required | Extensive training required | _[Score]_ | _[Plan]_ |
| **Change Management** | Easy implementation | Moderate workflow changes | Significant practice changes | _[Score]_ | _[Plan]_ |
| **Quality Monitoring** | Automated monitoring | Manual periodic review | Limited monitoring capability | _[Score]_ | _[Plan]_ |

## Risk Scoring and Classification

### Overall Risk Score Calculation
```
Total Risk Score = Σ(Risk Factor Score × Weight)

Weight Distribution:
- Patient Safety: 40%
- Bias and Fairness: 25%
- Privacy and Security: 20%
- Regulatory Compliance: 15%
```

**Total Risk Score**: _[Calculated Score]_ / 3.0

### Risk Classification
- **Low Risk** (1.0 - 1.5): Standard approval - should be straightforward
- **Medium Risk** (1.6 - 2.2): Enhanced review - expect more scrutiny and ongoing monitoring
- **High Risk** (2.3 - 3.0): Extensive validation - plan for significant time and resources

### Risk Tolerance Statement
_[Be honest about how much risk your organization is actually willing to accept for this type of system. Don't just copy generic language.]_

## Detailed Risk Analysis

### High-Priority Risks Identified
1. **Risk Name**: _[Specific risk]_
   - **Likelihood**: _[Low/Medium/High]_
   - **Impact**: _[Low/Medium/High]_
   - **Current Controls**: _[Existing mitigations]_
   - **Residual Risk**: _[Low/Medium/High]_

2. **Risk Name**: _[Specific risk]_
   - **Likelihood**: _[Low/Medium/High]_
   - **Impact**: _[Low/Medium/High]_
   - **Current Controls**: _[Existing mitigations]_
   - **Residual Risk**: _[Low/Medium/High]_

### Risk Mitigation Plan

#### Immediate Actions (0-30 days)
- [ ] _[Action item with owner and due date]_
- [ ] _[Action item with owner and due date]_
- [ ] _[Action item with owner and due date]_

#### Short-term Actions (1-6 months)
- [ ] _[Action item with owner and due date]_
- [ ] _[Action item with owner and due date]_
- [ ] _[Action item with owner and due date]_

#### Long-term Actions (6+ months)
- [ ] _[Action item with owner and due date]_
- [ ] _[Action item with owner and due date]_
- [ ] _[Action item with owner and due date]_

## Monitoring and Review Plan

### Continuous Monitoring Requirements
| Metric | Threshold | Monitoring Frequency | Alert Procedure |
|--------|-----------|---------------------|-----------------|
| **Model Performance** | _[Threshold]_ | _[Frequency]_ | _[Alert process]_ |
| **Bias Metrics** | _[Threshold]_ | _[Frequency]_ | _[Alert process]_ |
| **Clinical Outcomes** | _[Threshold]_ | _[Frequency]_ | _[Alert process]_ |
| **Security Events** | _[Threshold]_ | _[Frequency]_ | _[Alert process]_ |

### Periodic Review Schedule
- **Monthly**: Operational metrics review
- **Quarterly**: Risk assessment update
- **Annually**: Comprehensive risk reassessment
- **As Needed**: Incident-triggered review

## Stakeholder Approval

### Technical Review
**Lead Data Scientist**: _[Name and Signature]_ Date: _[Date]_  
**Clinical SME**: _[Name and Signature]_ Date: _[Date]_  
**Security Officer**: _[Name and Signature]_ Date: _[Date]_  

### Executive Approval
**Chief Medical Officer**: _[Name and Signature]_ Date: _[Date]_  
**Chief Technology Officer**: _[Name and Signature]_ Date: _[Date]_  
**Chief Compliance Officer**: _[Name and Signature]_ Date: _[Date]_  

### Risk Committee Approval
**Risk Committee Chair**: _[Name and Signature]_ Date: _[Date]_  
**Committee Decision**: _[Approved/Conditional/Rejected]_  
**Conditions**: _[Any conditions for approval]_  

## Appendices

### Appendix A: Regulatory References
- FDA Software as Medical Device Guidance
- HIPAA Privacy and Security Rules
- State-specific healthcare AI regulations
- Relevant clinical practice guidelines

### Appendix B: Technical Documentation
- Model architecture and training details
- Validation study results
- Bias testing methodology and results
- Security architecture documentation

### Appendix C: Clinical Evidence
- Literature review on clinical effectiveness
- Validation study protocols and results
- Clinical expert review comments
- Patient safety assessment

---

**Template Version**: 1.0  
**Last Updated**: 2024  
**Owner**: Risk Management Committee  
**Approval**: Chief Risk Officer