# Contributing to QuickMedCalc

Thank you for your interest in contributing to QuickMedCalc! This project benefits from both medical professionals and developers working together.

## Medical Disclaimer for Contributors

All contributors must understand that this software is for educational purposes and must not replace clinical judgment. Contributors are responsible for ensuring the accuracy of any medical calculations they add or modify.

## How to Contribute

### For Medical Professionals 👩‍⚕️👨‍⚕️

Your clinical expertise is invaluable! You can contribute without coding knowledge:

#### **Reporting Issues**
- Found an incorrect calculation? Please report it immediately
- Missing a calculator you use daily? Request it
- Interface confusing during clinical use? Let us know

#### **Calculator Validation**
- Verify formulas against current medical literature
- Test edge cases with real patient scenarios
- Suggest interpretations and clinical guidance

#### **Clinical Feedback**
- How can the workflow be improved?
- Which calculators are missing from your daily practice?
- What would make this more useful in clinical settings?

### For Developers 👩‍💻👨‍💻

#### **Code Contribution Process**

1. **Fork the Repository**
   ```bash
   git clone https://github.com/yourusername/QuickMedCalc.git
   cd QuickMedCalc
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/new-calculator-name
   ```

3. **Make Your Changes**
   - Follow the existing code structure
   - Add comprehensive comments
   - Include medical references in docstrings

4. **Test Thoroughly**
   ```bash
   python src/main.py
   # Test all new functionality
   ```

5. **Submit a Pull Request**
   - Provide clear description
   - Include medical references for new calculations
   - Tag relevant issues

#### **Code Standards**

##### **Medical Calculator Requirements**
Every new calculator MUST include:

```python
def create_new_calculator(self):
    """
    Calculator Name - Brief Description
    
    Medical Reference:
    - Primary source: [Journal/Guideline]
    - Formula validation: [Date checked]
    - Clinical context: [When to use]
    
    IMPORTANT: All calculations must be independently verified
    """
```

##### **Code Structure**
- Follow existing naming conventions
- Use descriptive variable names
- Include input validation
- Provide clear error messages
- Add result interpretation where appropriate

##### **Medical Validation**
```python
# Example of proper medical validation
def calculate_gcs(eye, verbal, motor):
    """
    Glasgow Coma Scale Calculator
    
    Reference: Teasdale & Jennett, Lancet 1974
    Validation: Cross-checked with current neurosurgical guidelines
    """
    # Input validation
    if not all(isinstance(x, int) for x in [eye, verbal, motor]):
        raise ValueError("All GCS components must be integers")
    
    if not (1 <= eye <= 4):
        raise ValueError("Eye opening must be 1-4")
    # ... additional validation
    
    total = eye + verbal + motor
    
    # Clinical interpretation based on current guidelines
    if total >= 13:
        interpretation = "Mild brain injury"
    # ... rest of interpretation
    
    return total, interpretation
```

#### **New Calculator Checklist**

- [ ] **Medical accuracy verified** against current literature
- [ ] **Edge cases handled** (invalid inputs, extreme values)
- [ ] **Clinical interpretations** included where appropriate
- [ ] **Proper error handling** with user-friendly messages
- [ ] **Consistent UI** following existing patterns
- [ ] **Database integration** for saving calculations
- [ ] **Documentation** in code and README
- [ ] **Testing** completed on multiple scenarios

### Adding New Calculators

#### **Step-by-Step Guide**

1. **Research the Calculator**
   - Find the original medical literature
   - Verify the current standard formula
   - Understand clinical context and limitations

2. **Add to Calculator Registry**
   ```python
   self.calculators = {
       # existing calculators...
       'new_calc': 'New Calculator Name'
   }
   ```

3. **Create Calculator Method**
   ```python
   def create_new_calculator(self):
       calc_frame, result_frame, notes_frame = self.create_calculator_frame("Calculator Title")
       # Implementation here
   ```

4. **Add to Load Function**
   ```python
   def load_calculator(self, calc_type):
       # existing conditions...
       elif calc_type == 'new_calc':
           self.create_new_calculator()
   ```

#### **Medical Reference Format**
```python
"""
MEDICAL REFERENCE:
Primary Source: Author et al. Journal Name. Year;Volume:Pages
Alternative Sources: [List any supporting references]
Last Verified: [Date]
Clinical Context: [When and why to use this calculator]
Limitations: [Known limitations or contraindications]
"""
```

## Testing Guidelines

### **For Medical Professionals**
- Test with real (anonymized) patient scenarios
- Verify against manual calculations
- Check edge cases (very high/low values)
- Ensure interpretations match clinical guidelines

### **For Developers**
```bash
# Run the application
python src/main.py

# Test each calculator with:
# - Normal values
# - Edge cases
# - Invalid inputs
# - Database saving functionality
```

## Submitting Issues

### **Bug Reports**
Include:
- Calculator name
- Input values used
- Expected vs actual result
- Medical reference supporting expected result

### **Feature Requests**
Include:
- Calculator name and medical use case
- Primary medical literature reference
- Frequency of use in clinical practice
- Target medical specialties

## Code Review Process

### **Medical Review**
All medical calculators require:
1. **Accuracy verification** by medical professional
2. **Literature validation** with current sources
3. **Clinical utility** assessment

### **Technical Review**
All code changes require:
1. **Code quality** review
2. **Testing** verification
3. **Documentation** completeness

## Community Guidelines

### **Be Respectful**
- Medical professionals and developers have different expertise
- Ask questions when unsure about medical or technical aspects
- Provide constructive feedback

### **Prioritize Patient Safety**
- Medical accuracy is the top priority
- When in doubt, don't merge
- Include appropriate disclaimers

### **Collaborate Effectively**
- Medical professionals: Provide clear clinical requirements
- Developers: Ask questions about medical context
- Everyone: Document decisions and reasoning

## Recognition

Contributors will be acknowledged in:
- README.md contributor section
- CHANGELOG.md for specific contributions
- Release notes for major contributions

## Getting Help

- **Medical Questions**: Tag medical professional contributors
- **Technical Questions**: Create GitHub issues
- **General Discussion**: Use GitHub Discussions

## Legal Considerations

By contributing, you agree that:
- Your contributions are your original work
- You grant permission for use under the MIT license
- You understand this is educational software only
- You accept no liability for clinical decisions made using this software

---

**Remember: We're building something that could help medical professionals provide better patient care. Take it seriously! 🏥**