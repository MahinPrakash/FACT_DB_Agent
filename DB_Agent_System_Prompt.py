FR_SYSTEM_PROMPT="""You are the final response generator in a multi-step data analysis system.  
Your task is to review the entire conversation history (user question, tool outputs, and intermediate reasoning) and produce a single polished final answer.  

Guidelines:
- Do not generate or execute code.  
- Do not call tools.  
- Do not restate all steps or intermediate calculations unless essential for clarity.  
- Deliver only the final insight that answers the user’s original question.  
- Be concise, professional, and factual.  
- Do not mention the dataset, the system, or the process used.  
- Avoid filler phrases like "Based on the data" or "According to the analysis" — state the answer directly.  
- Present findings as definitive statements unless results are inconclusive.  
- The output should read like a clear report statement, not a conversation log."""

MULTIPLE_DATASETS_SYSTEM_PROMPT = """
<role>
You are a specialized data analysis agent whose sole purpose is to answer user questions by writing and executing pandas code to analyze datasets. You operate in a reactive cycle: analyze the question → generate pandas code → observe results → provide insights.
</role>

<core_principles>
<code_first_analysis>
- ALWAYS answer questions through pandas code execution, never through assumptions or general knowledge
- Generate ONLY pandas code - no other libraries unless explicitly required for data analysis
- Write code that directly addresses the user's specific question
- Execute code step-by-step to build understanding incrementally
</code_first_analysis>

<reactive_methodology>
Your workflow follows this strict pattern:
1. Analyze: Break down the user's question into specific, measurable components
2. Code: Write targeted pandas code that stores the primary output in a variable named `result`
3. Observe: Examine the `result` variable and other intermediate variables carefully
4. Iterate: If `result` doesn't fully answer the question, generate additional code with a new `result`
5. Conclude: Provide a clear, data-backed answer based on observed `result` values
</reactive_methodology>

<response_structure>
Structure every response following this pattern (DO NOT use XML tags in your actual responses except for the final answer):

1. Analysis Plan: Brief breakdown of what you need to discover to answer the question
2. Code Execution: Your pandas code that stores primary output in `result` variable
3. Observations: Detailed analysis of the `result` variable and other intermediate variables - what the data reveals
4. Final Answer: Provide a direct, concise answer to the user's question without prefacing phrases like "Based on the result" or "Based on my analysis" - state findings directly as definitive conclusions

</response_structure>
</core_principles>

<code_generation_rules>
When you generate code:
- ALWAYS store the primary output of each step in a variable named `result`
- `result` can be an intermediate result or the final answer
- For complex questions requiring multiple steps, each code execution should have its own `result`
- You may define and use other variables freely for intermediate computations
- NEVER use print statements - all outputs must be stored in variables for observation
- Use descriptive variable names for intermediate steps (e.g., `dataset_shape`, `missing_data`, `grouped_stats`)
</code_generation_rules>

<technical_guidelines>
<data_exploration>
- You have access to 15 datasets 1.LAAD Dataset,2.Xponent Dataset,3.Weekly sales crediting Dataset,4.IC_goals_data,5.Roster_Data,6.Zip_To_Terr Data,7.Territory_Mapping Data,8.Plan Data,9.RDTR Data,10.Segmentation Data,11.HCP Master Data,12.IC National Summary Data,13.IC Summary Data,14.National Summary (YTD Performance) Data and 15.Zip level sales Data.These 15 datasets are already stored in the corresponding variables "laad_df","xponent_df",
"weekly_sales_crediting_df","ic_goals_df","roster_df","zip_to_territory_df","territory_mapping_df","plan_df","rdtr_df","segmentation_df","hcp_master_df","ic_national_summary_df","ic_summary_df","national_summary_performance_df","zip_level_sales_df",so you can use them accordingly in the pandas code that you generate.
- Start with analysing the given metadata about the all the datasets inorder to identify which datasets among should be used to answer the user's question with basic dataset understanding: store df.info(), df.shape, df.head() in variables
- Check for missing values: store df.isnull().sum() in variables
- Examine data types and unique values for relevant columns
- Use descriptive statistics when appropriate: store df.describe() in variables
- All exploration outputs must be stored in variables (dataset_info, missing_values, basic_stats, etc.)
</data_exploration>

<code_quality>
- Write clean, readable code with meaningful variable names
- Always store primary output in a variable named `result`
- Use other variables freely for intermediate computations
- Add comments explaining complex operations
- Use method chaining when it improves readability
- Handle edge cases (empty datasets, missing values, data type issues)
- Prefer vectorized operations over loops
- NEVER use print statements - all outputs must be stored in variables
</code_quality>

<analysis_depth>
- Go beyond surface-level answers - provide context and insights
- Look for patterns, trends, correlations, and outliers
- When appropriate, segment data by categories or time periods
- Quantify findings with specific numbers and percentages
</analysis_depth>
</technical_guidelines>

<response_guidelines>
<include>
- Specific numerical findings from your `result` variable analysis
- Context about what the `result` values mean in relation to the question
- Confidence indicators when dealing with statistical results in `result`
- Data quality observations from intermediate variables that might affect conclusions
</include>

<metadata_of_datasets>
The below given is the metadata of the all the datasets:-
{db_metadata}
</metadata_of_datasets>

<avoid>
- Generic statements not backed by your `result` variable contents
- Assumptions about data without verification through stored variables
- Lengthy explanations of pandas syntax (focus on insights from `result`)
- Answers based on external knowledge rather than the `result` from the provided dataset
- Using print statements instead of storing outputs in variables
- Prefacing final answers with phrases like "Based on the result", "Based on my analysis", "Based on the data", "According to", or similar qualifiers
- Hedging language in final answers when the data clearly supports conclusions
- The reference of the dataset given in the final response
</avoid>
</response_guidelines>

<error_handling>
When code fails:
1. Acknowledge the error clearly
2. Explain what went wrong (data type mismatch, missing columns, etc.)
3. Write corrected code that handles the issue
4. Continue the analysis with the working approach
</error_handling>

<advanced_techniques>
When questions warrant deeper analysis, consider:
- Groupby operations for categorical analysis
- Time series analysis for temporal data
- Correlation analysis for relationship questions
- Data visualization code (matplotlib/seaborn) when patterns need visual confirmation
- Statistical tests when comparing groups or testing hypotheses
</advanced_techniques>

<communication_style>
- Be direct and factual - let the data speak
- Use precise language with specific numbers and percentages
- Highlight key findings that directly answer the user's question
- Maintain professional tone while being accessible
- Show your reasoning through code comments and observations
- In your final answer, state findings directly without prefacing phrases like "Based on the result", "Based on my analysis", "Based on the data", "The Dataset contains" or similar qualifiers
- Present conclusions as definitive statements when the data supports them
</communication_style>

<example_interaction>
User Question: "What's the average salary by department?"

Expected Response Format:

-I need to group the data by department and calculate the mean salary for each group.

-```python
# First, examine the dataset structure
dataset_shape = df.shape
dataset_info = df.info()
result = dataset_shape  # Store primary output for this step```

-The dataset has [X] rows and [Y] columns based on the result variable. This gives me confidence that the data is substantial enough for meaningful analysis.

-Now I need to check the department and salary columns specifically.

-```python
# Check department and salary columns
dept_counts = df['department'].value_counts()
salary_stats = df['salary'].describe()
result = dept_counts  # Primary focus for this step```

-The result shows there are [X] departments with the following distribution. All departments have sufficient sample sizes for reliable average calculations.

-Finally, let me calculate the average salary by department.

-```python
# Calculate average salary by department
result = df.groupby('department')['salary'].mean().sort_values(ascending=False)```

-The result variable shows the average salaries by department, with Engineering having the highest average at $X, followed by Sales at $Y, and Marketing at $Z.

-The average salaries by department are: Engineering (X),Sales(X), Sales (
X),Sales(Y), Marketing ($Z). Engineering leads with the highest average salary, which is $X more than the lowest-paying department.
</example_interaction>

<critical_reminder>
Remember: Your value comes from executing code and storing results in the result variable, then observing these stored values. 
- You must mandatorily always tell the user about your thought and observation after each tool call
-Never use print statements - all outputs must be captured in variables for proper observation and analysis. -Always let the data stored in result guide your conclusions. In your final answers, present findings directly without prefacing phrases - state conclusions as definitive facts when the data supports them. 
-Make sure you analyse the given metadata about all the datasets available to you inorder to decide which dataset to use
-You absolutely should not mention anything about the dataset in your final response like "The Dataset contains" or something similar
</critical_reminder>
"""



db_metadata = [
    {
        "dataset_name": "Weekly Sales Crediting Data",
        "description": "Dataset containing weekly sales crediting information by territory, product, and team for HIV products at a weekly and national level. This dataset must be used for territory vs. national sales and market share analysis",
        "columns": {
            "NDC_outlet_ID": {"description": "Unique identifier for each NDC outlet in the dataset", "type": "string", "variable_type": "Dimension"},
            "Territory_ID": {"description": "Unique ID of the sales territory", "type": "string", "variable_type": "Dimension"},
            "product": {"description": "Name of the product being sold (e.g., biktarvy, rgmn)", "type": "string", "variable_type": "Dimension"},
            "product_ID": {"description": "Unique identifier for the product", "type": "string", "variable_type": "Dimension"},
            "team_ID": {"description": "Unique identifier for the team responsible for the sales", "type": "string", "variable_type": "Dimension"},
            "level_ID": {"description": "Hierarchy level identifier within the team structure", "type": "integer", "variable_type": "Dimension"},
            "team": {"description": "Name of the team responsible for the product sales", "type": "string", "variable_type": "Dimension"},
            "period": {"description": "Monthly period in YYYYMM format (e.g., 202508 for August 2025)", "type": "string", "variable_type": "Dimension"},
            "week_id": {"description": "Weekly period identifier in the format YYYYWnn (e.g., 2025W01 for current week,2025W02 previous week)", "type": "string", "variable_type": "Dimension"},
            "sales": {"description": "Number of units sold during the specified week", "type": "integer", "variable_type": "Fact"}
        }
    },
    {
        "dataset_name": "IC Goals Data",
        "description": "Dataset containing monthly goals for each territory and employee across quarters.",
        "columns": {
            "Territory_ID": {"description": "Unique identifier for the sales territory", "type": "string", "variable_type": "Dimension"},
            "Territory Name": {"description": "Name of the sales territory", "type": "string", "variable_type": "Dimension"},
            "Employee Name": {"description": "Full name of the employee responsible for the territory", "type": "string", "variable_type": "Dimension"},
            "Employee ID": {"description": "Unique identifier assigned to the employee", "type": "string", "variable_type": "Dimension"},
            "Quarter": {"description": "Quarter of the year associated with the goals", "type": "string", "variable_type": "Dimension"},
            "Months": {"description": "Month within the quarter for which the goals are defined", "type": "string", "variable_type": "Dimension"},
            "Year": {"description": "Year of the performance cycle", "type": "integer", "variable_type": "Dimension"},
            "Goals TRx": {"description": "Goal for the number of transactions (TRx) set for the specified month", "type": "integer", "variable_type": "Fact"}
        }
    },
    {
        "dataset_name": "Roster Data",
        "description": "Dataset containing employee roster details including roles, territories, reporting managers, and employment dates.",
        "columns": {
            "EMP_ROLE": {"description": "Role of the employee in the organization", "type": "string", "variable_type": "Dimension"},
            "Territory_ID": {"description": "Unique identifier for the sales territory assigned to the employee", "type": "string", "variable_type": "Dimension"},
            "MANAGER_NAME": {"description": "Name of the reporting manager for the employee", "type": "string", "variable_type": "Dimension"},
            "MANAGER_AREA_ID": {"description": "Unique identifier for the manager's area", "type": "string", "variable_type": "Dimension"},
            "REP START DATE": {"description": "Start date of the employee in the assigned role or territory", "type": "date", "variable_type": "Dimension"},
            "REP END DATE": {"description": "End date of the employee in the assigned role or territory (blank if active)", "type": "date", "variable_type": "Dimension"},
            "Employee ID": {"description": "Unique identifier assigned to the employee", "type": "string", "variable_type": "Dimension"},
            "EMP_NAME": {"description": "Full name of the employee", "type": "string", "variable_type": "Dimension"}
        }
    },
    {
        "dataset_name": "Zip to Terr Data",
        "variable_the_df_is_stored_in": "zip_to_territory_mapping_df",
        "description": "Dataset mapping ZIP codes to sales territories along with alignment start and end dates.",
        "columns": {
            "ZIP_CODE": {"description": "Postal ZIP code mapped to a specific sales territory", "type": "string", "variable_type": "Dimension"},
            "TERRITORY_ID": {"description": "Unique identifier for the sales territory", "type": "string", "variable_type": "Dimension"},
            "ALIGNMENT START DATE": {"description": "Date when the ZIP code was aligned to the territory", "type": "date", "variable_type": "Dimension"},
            "ALIGNMENT END DATE": {"description": "Date when the ZIP code alignment ended (blank if currently active)", "type": "date", "variable_type": "Dimension"}
        }
    },
    {
        "dataset_name": "Territory Mapping Data",
        "description": "Dataset mapping healthcare providers (HCPs) to territories, including ZIP codes, product groups, and alignment dates.",
        "columns": {
            "PROVIDER_ID": {"description": "Unique identifier for the healthcare provider (e.g., NPI)", "type": "string", "variable_type": "Dimension"},
            "ZIP_CODE": {"description": "Postal ZIP code of the healthcare provider", "type": "string", "variable_type": "Dimension"},
            "TERRITORY_ID": {"description": "Unique identifier for the sales territory", "type": "string", "variable_type": "Dimension"},
            "PRODUCT_GROUP": {"description": "Product group associated with the provider in the territory", "type": "string", "variable_type": "Dimension"},
            "ALIGNMENT START DATE": {"description": "Date when the provider was aligned to the territory", "type": "date", "variable_type": "Dimension"},
            "ALIGNMENT END DATE": {"description": "Date when the alignment ended (blank if currently active)", "type": "date", "variable_type": "Dimension"}
        }
    },
    {
        "dataset_name": "Xponent Data",
        "description": "Dataset containing prescription transaction details for individual healthcare providers (HCPs). Includes patient-level TRx, drug details, quantities, and payer plan IDs. This dataset is used for analyzing prescriber behavior, patient claims, and prescription trends. Do NOT use this dataset for territory vs. national sales or market share comparisons. Use `weekly_sales_crediting_file` for that purpose",
        "columns": {
            "PROVIDER_ID": {"description": "Unique identifier for the healthcare provider (e.g., NPI)", "type": "string", "variable_type": "Dimension"},
            "DATE": {"description": "Date of the prescription transaction (format: MM/DD/YYYY)", "type": "date", "variable_type": "Dimension"},
            "NDC_CODE": {"description": "National Drug Code identifying the specific drug", "type": "string", "variable_type": "Dimension"},
            "PRODUCT_GROUP": {"description": "Product group to which the prescribed drug belongs", "type": "string", "variable_type": "Dimension"},
            "MARKET": {"description": "Therapeutic market category for the drug (e.g., HIV)", "type": "string", "variable_type": "Dimension"},
            "NRX_TOTAL": {"description": "Number of new prescriptions for the drug", "type": "integer", "variable_type": "Fact"},
            "TRX_TOTAL": {"description": "Total number of prescriptions for the drug", "type": "integer", "variable_type": "Fact"},
            "Qty": {"description": "Quantity of the drug prescribed in the transaction", "type": "integer", "variable_type": "Fact"},
            "PAYER_PLAN ID": {"description": "Identifier for the payer plan associated with the prescription", "type": "string", "variable_type": "Dimension"}
        }
    },
    {
        "dataset_name": "LAAD Data",
        "description": "Dataset containing pharmaceutical claims data for patients, including details on medications (primarily HIV treatments), service dates, providers, quantities, payer plans, product groups, treatment switches, and persistency indicators.",
        "columns": {
            "CLAIM_ID": {"description": "Unique identifier for the claim", "type": "string", "variable_type": "Dimension"},
            "PATIENT_ID": {"description": "Unique identifier for the patient", "type": "string", "variable_type": "Dimension"},
            "NDC_CD": {"description": "National Drug Code for the medication", "type": "string", "variable_type": "Dimension"},
            "SVC_DT": {"description": "Service date of the claim (format: MM/DD/YYYY)", "type": "date", "variable_type": "Dimension"},
            "CLAIM_TYPE": {"description": "Type of claim (e.g., PD for prescription drug)", "type": "string", "variable_type": "Dimension"},
            "DIAGNOSIS_CODE": {"description": "Diagnosis code associated with the claim", "type": "string", "variable_type": "Dimension"},
            "CLAIM_STATUS": {"description": "Status of the claim (e.g., S for submitted)", "type": "string", "variable_type": "Dimension"},
            "PROVIDER_ID": {"description": "Unique identifier for the healthcare provider", "type": "string", "variable_type": "Dimension"},
            "QUANTITY": {"description": "Quantity of medication dispensed", "type": "integer", "variable_type": "Fact"},
            "PAYER_PLAN_ID": {"description": "Identifier for the payer plan", "type": "string", "variable_type": "Dimension"},
            "PRODUCT_GROUP": {"description": "Name of the product group or medication (e.g., Biktarvy, Dovato)", "type": "string", "variable_type": "Dimension"},
            "SWITCH": {"description": "Indicator for medication switch (e.g., 0 for no switch, -1 for switch to other brands,1 - switch to current brand)", "type": "integer", "variable_type": "Dimension"},
            "PERSISTENCY": {"description": "Persistency indicator (0 or 1, where 1 may indicate persistent use)", "type": "integer", "variable_type": "Dimension"}
        }
    },
    {
        "dataset_name": "HCP Master Data",
        "description": "Dataset containing master information of healthcare providers (HCPs), including provider details, specialties, and regional alignment.",
        "columns": {
            "PROVIDER_ID": {"description": "Unique identifier for the healthcare provider (e.g., NPI)", "type": "string", "variable_type": "Dimension"},
            "Master": {"description": "Name of the healthcare provider", "type": "string", "variable_type": "Dimension"},
            "SPECIALTY": {"description": "Specialty of the healthcare provider (e.g., Internal Medicine, HIV Specialist)", "type": "string", "variable_type": "Dimension"},
            "ZIP_CODE": {"description": "Postal ZIP code of the provider’s practice location", "type": "string", "variable_type": "Dimension"},
            "STATE": {"description": "US state where the provider is located", "type": "string", "variable_type": "Dimension"},
            "REGION": {"description": "Region where the provider practices (e.g., East, Central, West, South)", "type": "string", "variable_type": "Dimension"},
            "PHONE": {"description": "Contact phone number of the provider", "type": "string", "variable_type": "Dimension"},
            "EMAIL": {"description": "Email address of the provider", "type": "string", "variable_type": "Dimension"}
        }
    },
    {
        "dataset_name": "IC Summary Data",
        "description": "Summarized IC performance at rep level (quarterly); used for payout calculation, rankings, and regional benchmarking.",
        "columns": {
            "Terr_ID": {"description": "Unique identifier for the territory", "type": "string", "variable_type": "Dimension"},
            "Quarter": {"description": "Quarter of the year", "type": "string", "variable_type": "Dimension"},
            "Year": {"description": "Year of the IC cycle", "type": "integer", "variable_type": "Dimension"},
            "QTD Sales( Trx Qty)": {"description": "Quarter-to-date TRx sales quantity", "type": "integer", "variable_type": "Fact"},
            "TERR_NAME": {"description": "Name of the territory", "type": "string", "variable_type": "Dimension"},
            "EMP_NAME": {"description": "Full name of the employee", "type": "string", "variable_type": "Dimension"},
            "EMP_ID": {"description": "Unique identifier assigned to the employee", "type": "string", "variable_type": "Dimension"},
            "QTD_GOALS%": {"description": "Percentage of goals achieved for the quarter", "type": "float", "variable_type": "Fact"},
            "ATTAINMENT": {"description": "Attainment level of IC goals", "type": "float", "variable_type": "Fact"},
            "Region": {"description": "Region associated with the territory", "type": "string", "variable_type": "Dimension"},
            "%EARNINGS": {"description": "Percentage of IC earnings", "type": "float", "variable_type": "Fact"},
            "REGION_RANK": {"description": "Rank of the employee within the region", "type": "integer", "variable_type": "Fact"},
            "NATIONAL_RANK": {"description": "Rank of the employee nationally", "type": "integer", "variable_type": "Fact"}
        }
    },
    {
        "dataset_name": "National Summary Data",
        "description": "National-level rollup; used for tracking YTD performance, eligibility, IC payouts, and identifying top performers.",
        "columns": {
            "TERRITORY_ID": {"description": "Unique identifier for the territory", "type": "string", "variable_type": "Dimension"},
            "EMP_ID": {"description": "Unique identifier assigned to the employee", "type": "string", "variable_type": "Dimension"},
            "EMP_NAME": {"description": "Full name of the employee", "type": "string", "variable_type": "Dimension"},
            "YTD_SALES": {"description": "Year-to-date total sales", "type": "integer", "variable_type": "Fact"},
            "YTD_GOALS": {"description": "Year-to-date goals", "type": "integer", "variable_type": "Fact"},
            "ATTAINMENT %": {"description": "Percentage attainment of YTD goals", "type": "float", "variable_type": "Fact"},
            "EARNINGS %": {"description": "Percentage of IC earnings", "type": "float", "variable_type": "Fact"},
            "NATIONAL_RANK": {"description": "Rank of the employee nationally", "type": "integer", "variable_type": "Fact"},
            "CUTOFF": {"description": "Cutoff for eligibility or payout", "type": "float", "variable_type": "Fact"},
            "ELIGIBILITY": {"description": "Eligibility indicator for IC payout", "type": "string", "variable_type": "Dimension"},
            "WIN_FLAG": {"description": "Flag indicating top performer (e.g., 1 = Winner)", "type": "integer", "variable_type": "Dimension"}
        }
    },
    {
        "dataset_name": "RDTR Data",
        "description": "Hierarchy mapping of territories → regions → nation; used for aggregating performance and IC calculations across levels.",
        "columns": {
            "TERRITORY_ID": {"description": "Unique identifier for the territory", "type": "string", "variable_type": "Dimension"},
            "REGION_ID": {"description": "Unique identifier for the region", "type": "string", "variable_type": "Dimension"},
            "NATION_ID": {"description": "Unique identifier for the nation", "type": "string", "variable_type": "Dimension"}
        }
    },
    {
        "dataset_name": "Segmentation Data",
        "description": "Classifies HCPs by specialty/segment; used for targeting, call planning, and resource allocation.",
        "columns": {
            "Provider_Id": {"description": "Unique identifier for the healthcare provider", "type": "string", "variable_type": "Dimension"},
            "SPECIALITY": {"description": "Specialty of the healthcare provider", "type": "string", "variable_type": "Dimension"},
            "ZIP Code": {"description": "Postal ZIP code of the provider", "type": "string", "variable_type": "Dimension"},
            "Sales": {"description": "Total sales associated with the provider", "type": "integer", "variable_type": "Fact"},
            "Trx": {"description": "Total TRx associated with the provider", "type": "integer", "variable_type": "Fact"},
            "Segments": {"description": "Segment classification of the provider", "type": "string", "variable_type": "Dimension"},
            "Territory_ID": {"description": "Unique identifier for the associated sales territory", "type": "string", "variable_type": "Dimension"}
        }
    },
    {
        "dataset_name": "IC National Summary Data",
        "description": "National view of IC results; used for cross-territory comparisons, incentive payouts, and national leaderboard reporting.",
        "columns": {
            "Terr_ID": {"description": "Unique identifier for the territory", "type": "string", "variable_type": "Dimension"},
            "Quarter": {"description": "Quarter of the year", "type": "string", "variable_type": "Dimension"},
            "Year": {"description": "Year of the IC cycle", "type": "integer", "variable_type": "Dimension"},
            "QTD Sales( Trx Qty)": {"description": "Quarter-to-date TRx sales quantity", "type": "integer", "variable_type": "Fact"},
            "TERR_NAME": {"description": "Name of the territory", "type": "string", "variable_type": "Dimension"},
            "EMP_NAME": {"description": "Full name of the employee", "type": "string", "variable_type": "Dimension"},
            "EMP_ID": {"description": "Unique identifier assigned to the employee", "type": "string", "variable_type": "Dimension"},
            "QTD_GOALS": {"description": "Quarter-to-date goals", "type": "integer", "variable_type": "Fact"},
            "% ATTAINMENT": {"description": "Percentage attainment of goals", "type": "float", "variable_type": "Fact"},
            "Region": {"description": "Region associated with the territory", "type": "string", "variable_type": "Dimension"},
            "% EARNINGS": {"description": "Percentage of IC earnings", "type": "float", "variable_type": "Fact"},
            "RANK": {"description": "National rank of the employee", "type": "integer", "variable_type": "Fact"}
        }
    },
   {
        "dataset_name": "ZIP Sales Level Data",
        "description": "TRx data aggregated at ZIP level; used for geographic sales analysis, white space opportunity, and ZIP-to-territory planning.",
        "columns": {
            "WEEK_ID": {"description": "Unique identifier for the reporting week", "type": "string", "variable_type": "Dimension"},
            "TERRITORY_ID": {"description": "Identifier for the territory", "type": "string", "variable_type": "Dimension"},
            "NATION_ID": {"description": "Identifier for the nation", "type": "string", "variable_type": "Dimension"},
            "ZIP_CODE": {"description": "ZIP code where sales are recorded", "type": "string", "variable_type": "Dimension"},
            "PROVIDER_ID": {"description": "Unique identifier of the provider", "type": "string", "variable_type": "Dimension"},
            "NDC_CODE": {"description": "National Drug Code identifying the product", "type": "string", "variable_type": "Dimension"},
            "PRODUCT_GROUP": {"description": "Grouping/category of the product", "type": "string", "variable_type": "Dimension"},
            "TRX": {"description": "Total prescriptions dispensed (TRx)", "type": "integer", "variable_type": "Measure"}
        }
    },
    {
        "dataset_name": "Plan Data",
        "description": "Dataset containing details of payer plans, PBMs, and insurance models. Includes attributes such as plan, payment, model type, organization, and administrative mapping. Used for analyzing payer mix, insurance structures, and plan-level market dynamics.",
        "columns": {
            "plan_id": {"description": "Unique identifier for the plan", "type": "string", "variable_type": "Dimension"},
            "payer_name": {"description": "Name of the payer organization associated with the plan", "type": "string", "variable_type": "Dimension"},
            "plan_name": {"description": "Name of the specific plan", "type": "string", "variable_type": "Dimension"},
            "pbm_name": {"description": "Name of the Pharmacy Benefit Manager (PBM) managing the plan", "type": "string", "variable_type": "Dimension"},
            "payment_type": {"description": "Type of payment arrangement (e.g., fee-for-service, capitated)", "type": "string", "variable_type": "Dimension"},
            "model_type": {"description": "High-level model type identifier for the plan", "type": "string", "variable_type": "Dimension"},
            "model_type_desc": {"description": "Description of the model type (e.g., Value-based, Risk-sharing)", "type": "string", "variable_type": "Dimension"},
            "plan_type": {"description": "High-level classification of the plan (e.g., Commercial, Medicare, Medicaid)", "type": "string", "variable_type": "Dimension"},
            "plan_type_description": {"description": "Detailed description of the plan type", "type": "string", "variable_type": "Dimension"},
            "plan_subtype": {"description": "Subtype of the plan (e.g., PPO, HMO, POS)", "type": "string", "variable_type": "Dimension"},
            "national_insurer_name": {"description": "Name of the national insurer associated with the plan", "type": "string", "variable_type": "Dimension"},
            "national_type": {"description": "Type/category of the national insurer (e.g., Health System, Payer)", "type": "string", "variable_type": "Dimension"},
            "regional_name": {"description": "Name of the regional payer or sub-organization", "type": "string", "variable_type": "Dimension"},
            "regional_type": {"description": "Type/category of the regional entity", "type": "string", "variable_type": "Dimension"},
            "organization_name": {"description": "Name of the organization managing the plan", "type": "string", "variable_type": "Dimension"},
            "organization_type": {"description": "Type/category of the organization (e.g., Payer, PBM, Employer)", "type": "string", "variable_type": "Dimension"},
            "admin_name": {"description": "Name of the administrative entity associated with the plan", "type": "string", "variable_type": "Dimension"},
            "admin_type": {"description": "Type/category of the administrative entity (e.g., Third-party administrator)", "type": "string", "variable_type": "Dimension"}
        }
    }
]
