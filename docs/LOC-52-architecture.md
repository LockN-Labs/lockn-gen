# LOC-52-architecture.md

## Swashbuckle Configuration
1. Install Swashbuckle.AspNetCore via NuGet
2. Configure in Program.cs with:
   - AddSwaggerGen()
   - UseSwagger()
   - UseSwaggerUI()
3. Enable XML comments with IncludeXmlComments()

## XML Documentation Setup
1. Add <GenerateDocumentationFile>True</GenerateDocumentationFile> to csproj
2. Add XML comment files for:
   - Models
   - DTOs
   - Endpoints
3. Configure XML file paths in SwaggerGen options

## Endpoint Grouping Strategy
1. Use [GroupName] attribute for:
   - Receipts (v1-receipts)
   - Budgets (v1-budgets)
   - Users (v1-users)
2. Configure Swagger to display groups in UI

## Required File Modifications
1. LockNLogger.Api.csproj
2. Program.cs
3. ReceiptEndpoints.cs
4. BudgetEndpoints.cs
5. Swagger configuration file (if created)