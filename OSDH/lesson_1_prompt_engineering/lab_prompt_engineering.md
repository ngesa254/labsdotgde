# Effective Prompting Workshop Guide
## Open Digital Health Summit '24: Building with FHIR Track

### Step 1: Define the Task and Persona

**Template Prompt:**
```
You are a [role] with expertise in [specific domain]. You understand how to [key capability] that is appropriate for [context/audience].
```

**Example for our Context:**
```
You are a senior FHIR architect with extensive experience implementing health information systems in Africa. You understand how to design interoperable healthcare solutions that are appropriate for low-resource settings and align with WHO guidelines.
```

### Step 2: Set the Tone and Do Ideation

**Template Prompt:**
```
You are a [role] with [expertise].
You should write in a tone that is [technical/practical/explanatory].
Can you give me 5 ideas about [specific FHIR implementation challenge]?
```

**Example for our Context:**
```
You are a senior FHIR architect with experience in African healthcare systems.
You should write in a tone that is technical yet practical for implementers.
Can you give me 5 ideas for implementing offline-capable FHIR systems for rural clinics in Kenya where internet connectivity is unstable? Each solution should consider local infrastructure constraints and ensure data integrity.
```

### Step 3: Structure with Background Information

**Template Prompt:**
```
You are a [role] with [expertise].
You should write in a tone that is [style].
I would like the [documentation/solution] to have the following sections:
1. Overview/Architecture
2. Implementation Approach
3. Technical Requirements
4. Integration Points
5. Considerations for Low-Resource Settings
```

**Example for our Context:**
```
You are a senior FHIR architect with experience in African healthcare systems.
You should write in a tone that is technical yet practical for implementers.
I would like you to create documentation for implementing SMART Guidelines for immunization tracking that includes:
1. Overview of FHIR resources needed for immunization tracking
2. Implementation approach using the Android FHIR SDK
3. Technical requirements including offline capabilities
4. Integration points with existing health systems
5. Considerations for rural clinic settings
```

### Step 4: Add Examples and Details

**Template with Example:**
```
Here's an example of how the implementation should work:
<example>
When a healthcare worker opens the app offline, they should be able to:
1. View existing patient immunization records
2. Record new immunizations using FHIR Immunization resource
3. Queue changes for sync when connectivity returns
</example>
```

### Step 5: Include Thinking Instructions

**Example for our Context:**
```
Think through this step-by-step and consider:
- What FHIR resources are essential for minimum viable functionality?
- How will data be synchronized when connectivity returns?
- What validation rules need to work offline?
Place your thinking for each component in <thinking> tags.
```

### Step 6: Specify Output Format

```markdown
Write the technical specification in markdown format with:
- Clear headings for each section
- Code examples in appropriate blocks
- Architecture diagrams (if needed)
Include an executive summary suitable for presentation to Ministry of Health stakeholders.
```

## Best Practices for Prompting in Healthcare Context:

1. **Be Specific About Standards**
   - Mention specific FHIR versions
   - Reference relevant Implementation Guides
   - Specify which profiles should be used

2. **Consider Local Context**
   - Include requirements for offline operation
   - Address low-resource settings
   - Consider local regulatory requirements

3. **Think About Scale**
   - Consider national-level implementations
   - Address multi-facility deployments
   - Plan for future extensibility

4. **Address Integration**
   - Specify integration with existing systems
   - Consider national health information exchanges
   - Plan for cross-border scenarios

## Workshop Exercise:

Let's practice by creating a prompt for a real-world scenario:

**Scenario:** You need to create documentation for implementing a FHIR-based maternal health tracking system that works in both urban and rural settings in Kenya.

**Your Turn:** Using the template below, craft a prompt that would help you get the most useful response:

```
You are a [role]...
You understand how to [capability]...
Please create [deliverable] with the following sections...
Consider these specific requirements...
Include examples of...
```

### Example Solution:

```
You are a FHIR implementation specialist with experience in maternal health systems.
You understand how to design offline-capable FHIR applications that work in low-resource settings.
Please create technical documentation for a maternal health tracking system with the following sections:
1. Core FHIR resources and profiles for maternal health
2. Offline data collection and synchronization approach
3. Integration with existing DHIS2 systems
4. Security and privacy considerations
5. Implementation guide for rural clinics

Consider these specific requirements:
- Must work offline for up to 1 week
- Support both SMS and app-based data collection
- Integrate with national health information exchange
- Support WHO SMART Guidelines for maternal health

Include examples of:
- FHIR resource instances for key maternal health data
- Synchronization protocols
- Error handling approaches
```

## Conclusion

Remember that effective prompting for healthcare implementations requires:
- Clear understanding of technical requirements
- Consideration of local context
- Attention to standards and interoperability
- Focus on practical implementation details

These skills will be particularly valuable as you work to implement FHIR-based solutions in your own contexts.