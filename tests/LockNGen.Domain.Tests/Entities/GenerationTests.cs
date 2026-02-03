using FluentAssertions;
using LockNGen.Domain.Entities;
using Xunit;

namespace LockNGen.Domain.Tests.Entities;

public class GenerationTests
{
    [Fact]
    public void Generation_ShouldHaveDefaultValues()
    {
        // Act
        var generation = new Generation();

        // Assert
        generation.Id.Should().NotBeEmpty();
        generation.Prompt.Should().BeEmpty();
        generation.Model.Should().Be("sdxl");
        generation.Width.Should().Be(1024);
        generation.Height.Should().Be(1024);
        generation.Steps.Should().Be(20);
        generation.Guidance.Should().Be(7.5);
        generation.Status.Should().Be(GenerationStatus.Queued);
        generation.CreatedAt.Should().BeCloseTo(DateTime.UtcNow, TimeSpan.FromSeconds(1));
    }

    [Fact]
    public void Generation_ShouldAcceptCustomPrompt()
    {
        // Arrange
        var prompt = "A beautiful sunset over mountains";

        // Act
        var generation = new Generation { Prompt = prompt };

        // Assert
        generation.Prompt.Should().Be(prompt);
    }

    [Theory]
    [InlineData(GenerationStatus.Queued)]
    [InlineData(GenerationStatus.Processing)]
    [InlineData(GenerationStatus.Completed)]
    [InlineData(GenerationStatus.Failed)]
    public void GenerationStatus_ShouldHaveAllExpectedValues(GenerationStatus status)
    {
        // Act
        var generation = new Generation { Status = status };

        // Assert
        generation.Status.Should().Be(status);
    }
}
