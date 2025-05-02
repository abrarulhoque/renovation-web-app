// Form validation and dynamic behavior for the bathroom renovation quote form

document.addEventListener('DOMContentLoaded', function () {
  // Initialize tooltips
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  )
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })

  // Automatic floor area calculation
  const widthInput = document.querySelector('#bathroom_details-width')
  const lengthInput = document.querySelector('#bathroom_details-length')
  const floorAreaInput = document.querySelector('#bathroom_details-floor_area')

  function calculateFloorArea () {
    if (widthInput && lengthInput && floorAreaInput) {
      const width = parseFloat(widthInput.value) || 0
      const length = parseFloat(lengthInput.value) || 0
      const area = ((width * length) / 10000).toFixed(2) // Convert from cm² to m²
      floorAreaInput.value = area
    }
  }

  if (widthInput && lengthInput) {
    widthInput.addEventListener('input', calculateFloorArea)
    lengthInput.addEventListener('input', calculateFloorArea)
  }

  // Show/hide related fields based on checkbox states
  function setupCheckboxDependencies () {
    const dependencies = {
      'bathroom_details-has_sketch': '#sketchUpload',
      'appliances-ceiling_lowering': '#spotlightsSection',
      'tiles_and_painting-paint_ceiling': '#ceilingPaintingHours',
      'tiles_and_painting-paint_walls': '#wallPaintingHours'
    }

    for (const [checkboxId, targetSelector] of Object.entries(dependencies)) {
      const checkbox = document.querySelector(`#${checkboxId}`)
      const target = document.querySelector(targetSelector)

      if (checkbox && target) {
        function toggleVisibility () {
          target.style.display = checkbox.checked ? 'block' : 'none'
        }
        checkbox.addEventListener('change', toggleVisibility)
        toggleVisibility() // Initial state
      }
    }
  }

  setupCheckboxDependencies()

  // Form validation
  const form = document.querySelector('form')
  if (form) {
    // Ensure CSRF token is refreshed if needed
    function refreshCsrfToken () {
      const csrfMeta = document.querySelector('meta[name="csrf-token"]')
      if (csrfMeta) {
        const csrfToken = csrfMeta.getAttribute('content')
        if (csrfToken) {
          const csrfInputs = document.querySelectorAll(
            'input[name="csrf_token"]'
          )
          csrfInputs.forEach(input => {
            input.value = csrfToken
          })
          console.log('CSRF token refreshed')
        } else {
          console.warn('CSRF token meta tag exists but has no content')
        }
      } else {
        console.warn('No CSRF token meta tag found')
      }
    }

    // Attempt to refresh token before form submission
    form.addEventListener('submit', function (event) {
      // Only validate client-side - let the server handle CSRF validation
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()

        // Find the first invalid input
        const invalidInput = form.querySelector(':invalid')
        if (invalidInput) {
          // Find the parent accordion item
          const accordionItem = invalidInput.closest('.accordion-item')
          if (accordionItem) {
            // Expand the accordion item
            const accordionButton =
              accordionItem.querySelector('.accordion-button')
            const accordionCollapse = accordionItem.querySelector(
              '.accordion-collapse'
            )
            if (accordionButton && accordionCollapse) {
              accordionButton.classList.remove('collapsed')
              accordionCollapse.classList.add('show')
            }
            // Scroll to the invalid input
            invalidInput.scrollIntoView({ behavior: 'smooth', block: 'center' })
          }
        }

        form.classList.add('was-validated')
      } else {
        // Form is valid, ensure the CSRF token is included
        refreshCsrfToken()

        // Log form submission for debugging
        console.log('Submitting form with valid data')

        // IMPORTANT: Do not prevent default or stop propagation here
        // Let the form submit normally to trigger the file download
      }
    })
  }

  // Dynamic form updates based on dwelling type
  const dwellingTypeInputs = document.querySelectorAll(
    'input[name="personal_details-dwelling_type"]'
  )
  const elevatorSection = document.querySelector('#elevatorSection')
  const parkingSection = document.querySelector('#parkingSection')

  dwellingTypeInputs.forEach(input => {
    input.addEventListener('change', function () {
      if (this.value === 'apartment') {
        elevatorSection.style.display = 'block'
        parkingSection.style.display = 'block'
      } else if (this.value === 'house') {
        elevatorSection.style.display = 'none'
        parkingSection.style.display = 'none'
      }
    })
  })

  // Price calculation functions
  function calculateSeasonCost () {
    // I. General Project & Site Conditions - Season
    let laborCost = 0
    const season = document.querySelector('#personal_details-season')?.value
    if (season === 'winter') {
      laborCost += 3000
    }
    return laborCost
  }

  function calculateGeneralConditionsCosts () {
    let laborCost = 0

    // Number of Floors
    const floorCount =
      parseInt(
        document.querySelector('#personal_details-floor_count')?.value
      ) || 0
    laborCost += floorCount * 100

    // Dwelling Type
    const dwellingType = document.querySelector(
      'input[name="personal_details-dwelling_type"]:checked'
    )?.value
    if (
      dwellingType === 'apartment' ||
      dwellingType === 'rental' ||
      dwellingType === 'commercial'
    ) {
      laborCost += 2000
    }

    // Cost for bringing in materials
    if (document.querySelector('#appliances-bring_in_materials')?.checked) {
      laborCost += 500 // Example cost, should match backend
    }

    return laborCost
  }

  function calculateAccessibilityCosts () {
    let laborCost = 0
    let otherCosts = 0

    // Parking Availability
    const parkingDistanceValue = document.querySelector(
      '#personal_details-parking_distance'
    )?.value
    if (parkingDistanceValue === 'bad') {
      laborCost += 1000
    } else if (parkingDistanceValue === 'ok') {
      laborCost += 500 // Example cost for 'ok'
    }
    // No cost for 'good'

    // Transport Possibility
    const transport = document.querySelector(
      '#personal_details-transport_possibility'
    )?.value
    if (transport === 'poor') {
      laborCost += 2000
    } else if (transport === 'ok') {
      laborCost += 500
    }

    // Parking Cost
    const parkingFee =
      parseFloat(
        document.querySelector('#personal_details-parking_fee')?.value
      ) || 0
    otherCosts += parkingFee

    // Service Car
    const serviceCarPrice =
      parseFloat(
        document.querySelector('#personal_details-service_car_price')?.value
      ) || 0
    const serviceCarDays =
      parseInt(
        document.querySelector('#personal_details-service_car_days')?.value
      ) || 0
    otherCosts += serviceCarPrice * serviceCarDays

    // Congestion Tax
    const congestionCharge =
      parseFloat(
        document.querySelector('#personal_details-congestion_charge')?.value
      ) || 0
    otherCosts += congestionCharge

    // Elevator
    const hasElevator = document.querySelector(
      '#personal_details-has_elevator'
    )?.value
    if (hasElevator === 'no') {
      laborCost += 2000
    }

    // Elevator Size
    const elevatorSize = document.querySelector(
      '#personal_details-elevator_size'
    )?.value
    if (elevatorSize === 'small') {
      laborCost += 2000
    } else if (elevatorSize === 'medium') {
      laborCost += 500
    }

    // Stairwell Access
    const goodStairwell = document.querySelector(
      '#personal_details-good_stairwell_access'
    )?.checked
    if (!goodStairwell) {
      laborCost += 2000
    }

    // Indoor Workspace
    const indoorWorkspace = document.querySelector(
      '#personal_details-indoor_workspace'
    )?.checked
    if (!indoorWorkspace) {
      laborCost += 2000

      // Workspace Distance
      const workspaceDistance =
        parseFloat(
          document.querySelector('#personal_details-workspace_distance')?.value
        ) || 0
      laborCost += workspaceDistance * 480
    }

    // Workspace Distance from Entry
    const entranceDistance =
      parseFloat(
        document.querySelector('#personal_details-entrance_distance')?.value
      ) || 0
    laborCost += entranceDistance * 480

    return { laborCost, otherCosts }
  }

  function calculateFloorProtectionCosts () {
    let laborCost = 0
    let materialCost = 0

    // Floor Protection (Hours)
    const hours =
      parseInt(
        document.querySelector('#appliances-floor_covering_time')?.value
      ) || 0
    laborCost += hours * 680

    // Floor Protection (Material)
    const floorArea =
      parseFloat(
        document.querySelector('#bathroom_details-floor_area')?.value
      ) || 0
    materialCost += floorArea * 50

    return { laborCost, materialCost }
  }

  function calculateBathroomDimensionCosts () {
    const width =
      parseFloat(document.querySelector('#bathroom_details-width')?.value) || 0
    const length =
      parseFloat(document.querySelector('#bathroom_details-length')?.value) || 0
    const height =
      parseFloat(document.querySelector('#bathroom_details-height')?.value) || 0

    // Base Labor Cost
    const basicLabor = 40000 + width * 160 + length * 160 + height * 160

    // Base Material Cost
    const basicMaterials = 20000 + width * 10 + length * 10 + height * 10

    return { basicLabor, basicMaterials }
  }

  function calculateLayoutModificationCosts () {
    let laborCost = 0
    let materialCost = 0

    // Sketch Provided
    const hasSketch = document.querySelector(
      '#bathroom_details-has_sketch'
    )?.checked
    if (hasSketch) {
      laborCost += 500 // Assuming a value for O73
    }

    // Number of Relocations
    const relocations =
      parseInt(
        document.querySelector('#bathroom_details-relocation_count')?.value
      ) || 0
    if (relocations === 1) {
      laborCost += 3000
      materialCost += 500
    } else if (relocations === 2) {
      laborCost += 6000
      materialCost += 1000
    } else if (relocations === 3) {
      laborCost += 8000
      materialCost += 1500
    }

    // Specific Fixture Relocations
    const fixtures = [
      { id: 'toilet_relocation', labor: 1000, material: 500 },
      { id: 'sink_relocation', labor: 1000, material: 500 },
      { id: 'shower_relocation', labor: 1000, material: 500 },
      { id: 'bathtub_relocation', labor: 1000, material: 1000 },
      { id: 'towel_warmer_relocation', labor: 1000, material: 400 }
    ]

    fixtures.forEach(fixture => {
      const value =
        parseInt(
          document.querySelector(`#bathroom_details-${fixture.id}`)?.value
        ) || 0
      if (value > 0) {
        laborCost += fixture.labor
        materialCost += fixture.material
      }
    })

    return { laborCost, materialCost }
  }

  function calculatePlumbingCosts () {
    let laborCost = 0
    let materialCost = 0

    // Floor Drain Replacement
    const drainReplacements =
      parseInt(
        document.querySelector('#bathroom_details-floor_drain_replacements')
          ?.value
      ) || 0
    if (drainReplacements === 1) {
      laborCost += 2500
      materialCost += 500
    } else if (drainReplacements === 2) {
      laborCost += 4500
      materialCost += 1000
    } else if (drainReplacements === 3) {
      laborCost += 6000
      materialCost += 1200
    }

    // Floor Drain Relocation
    const drainRelocation =
      parseInt(
        document.querySelector('#bathroom_details-floor_drain_relocation')
          ?.value
      ) || 0
    if (drainRelocation === '1') {
      laborCost += 1000
      materialCost += 500
    } else if (drainRelocation === '2') {
      laborCost += 2000
      materialCost += 1000
    } else if (drainRelocation === '3') {
      laborCost += 2500
      materialCost += 1500
    }

    // Extra Floor Drain
    if (
      document.querySelector('#bathroom_details-extra_floor_drain')?.checked
    ) {
      laborCost += 2500
      materialCost += 1000
    }

    // Channel Cutting
    if (document.querySelector('#bathroom_details-cut_channels')?.checked) {
      laborCost += 100
    }

    // Other Floor Penetrations
    const floorPenetrations =
      document.querySelector('#bathroom_details-floor_penetrations')?.value ||
      '0'
    if (floorPenetrations === '1') {
      laborCost += 500
      materialCost += 500
    } else if (floorPenetrations === '2') {
      laborCost += 1000
      materialCost += 1000
    } else if (floorPenetrations === '3') {
      laborCost += 1500
      materialCost += 1500
    }

    // Relocate Wall Penetrations
    const wallPenetrations =
      document.querySelector('#bathroom_details-wall_penetrations')?.value ||
      '0'
    if (wallPenetrations === '1') {
      laborCost += 2500
      materialCost += 1500
    } else if (wallPenetrations === '2') {
      laborCost += 5000
      materialCost += 2500
    } else if (wallPenetrations === '3') {
      laborCost += 7000
      materialCost += 4000
    }

    // Replace Floor Drain Pipes
    if (document.querySelector('#bathroom_details-move_drain_pipes')?.checked) {
      laborCost += 2500
      materialCost += 1000
    }

    // Water Shutoff Location
    const waterShutoff =
      document.querySelector('#appliances-water_shutoff')?.value || ''
    if (waterShutoff.toLowerCase().includes('association')) {
      laborCost += 1000
    }

    // Hidden Pipes
    if (
      document.querySelector('#interior_fittings-hidden_pipelines')?.checked
    ) {
      laborCost += 9000
      materialCost += 3000
    }

    // Hidden Ceiling Shower
    if (
      document.querySelector('#interior_fittings-hidden_ceiling_shower')
        ?.checked
    ) {
      laborCost += 8000
      materialCost += 2500
    }

    // Hidden Mixers
    const mixersCount =
      parseInt(
        document.querySelector('#interior_fittings-concealed_mixers_count')
          ?.value
      ) || 0
    const mixersPrice =
      parseFloat(
        document.querySelector('#interior_fittings-concealed_mixers_price')
          ?.value
      ) || 0
    if (mixersCount > 0) {
      laborCost += mixersCount * mixersPrice
      materialCost += 2500
    }

    // Save Existing Water Floor Heating
    if (
      document.querySelector('#interior_fittings-save_waterheated_floor')
        ?.checked
    ) {
      laborCost += 5000
      materialCost += 1000
    }

    // New Water Floor Heating
    if (
      document.querySelector('#interior_fittings-new_waterheated_floor')
        ?.checked
    ) {
      const floorArea =
        parseFloat(
          document.querySelector('#bathroom_details-floor_area')?.value
        ) || 0
      laborCost += 5000 + floorArea * 2000
      materialCost += 10000
    }

    return { laborCost, materialCost }
  }

  function calculateElectricalCosts () {
    let laborCost = 0
    let materialCost = 0

    // RCD / Ground Fault Interrupter
    const hasGFCI = document.querySelector('#appliances-rcd')?.checked
    if (!hasGFCI) {
      laborCost += 2000
      materialCost += 500
    }

    // Fusebox Distance
    const fuseBoxDistance =
      document.querySelector('#appliances-fusebox_distance')?.value || ''
    if (fuseBoxDistance === 'up_to_10m') {
      laborCost += 1000
      materialCost += 500
    } else if (fuseBoxDistance === 'another_floor') {
      laborCost += 2000
      materialCost += 1000
    }

    // Junction Box Distance
    const junctionBoxDistanceValue =
      document.querySelector('#appliances-junction_box_distance')?.value || ''
    if (junctionBoxDistanceValue === 'far') {
      laborCost += 1000
      materialCost += 500
    }

    // Electric Towel Warmer
    if (document.querySelector('#appliances-electric_towel_warmer')?.checked) {
      laborCost += 1500
      materialCost += 500
    }

    // Electric Floor Heating
    if (document.querySelector('#appliances-floor_heating')?.checked) {
      const floorArea =
        parseFloat(
          document.querySelector('#bathroom_details-floor_area')?.value
        ) || 0
      laborCost += 7000
      materialCost += floorArea * 1000
    }

    // Washing Machine
    if (document.querySelector('#appliances-washing_machine')?.checked) {
      laborCost += 4400
      materialCost += 1000
    }

    // Dryer
    if (document.querySelector('#appliances-dryer')?.checked) {
      laborCost += 2000
      materialCost += 500
    }

    // Sink Outlet
    if (document.querySelector('#appliances-sink_outlet')?.checked) {
      laborCost += 500
      materialCost += 500
    }

    // Iron Outlet
    if (document.querySelector('#appliances-iron_outlet')?.checked) {
      laborCost += 500
      materialCost += 500
    }

    // Spotlights
    const spotlightsCount =
      parseInt(document.querySelector('#appliances-spotlights_count')?.value) ||
      0
    const spotlightsPrice =
      parseFloat(
        document.querySelector('#appliances-spotlights_price_per_unit')?.value
      ) || 500 // Default price if not set
    if (spotlightsCount > 0) {
      laborCost += spotlightsCount * spotlightsPrice
      materialCost += spotlightsCount * 300 // Keep material cost separate unless specified otherwise
    }

    return { laborCost, materialCost }
  }

  function calculateFixturesCosts () {
    let laborCost = 0
    let materialCost = 0

    // Ceiling Lowering
    if (document.querySelector('#appliances-ceiling_lowering')?.checked) {
      const width =
        parseFloat(document.querySelector('#bathroom_details-width')?.value) ||
        0
      const length =
        parseFloat(document.querySelector('#bathroom_details-length')?.value) ||
        0
      laborCost += 2800 + width * length * 0.02
      materialCost += 1200
    }

    // Built-in Mirror
    if (document.querySelector('#interior_fittings-built_in_mirror')?.checked) {
      laborCost += 2500
    }

    // Build Shower Wall
    if (document.querySelector('#interior_fittings-shower_wall')?.checked) {
      laborCost += 12000
      materialCost += 2500
    }

    // Glass Block Wall
    if (
      document.querySelector('#interior_fittings-glass_block_wall')?.checked
    ) {
      laborCost += 12000
      materialCost += 4000
    }

    // Mount Glass Shower Wall
    if (
      document.querySelector('#interior_fittings-glass_shower_wall')?.checked
    ) {
      laborCost += 500
    }

    // Mount Shower Doors
    if (document.querySelector('#interior_fittings-shower_doors')?.checked) {
      laborCost += 1000
    }

    // Shower Drain Type
    const showerDrain = document.querySelector(
      '#interior_fittings-shower_drain'
    )?.value
    if (showerDrain === 'elongated') {
      laborCost += 2000
    }

    // Bathtub Type
    if (
      document.querySelector('#interior_fittings-bathtub_built_in')?.checked
    ) {
      laborCost += 15000
      materialCost += 2000
    }

    // Toilet Type
    if (
      document.querySelector('#interior_fittings-toilet_wall_mounted')?.checked
    ) {
      laborCost += 6500
      materialCost += 2000
    }

    // Inner Door Casing Replacement
    if (
      document.querySelector('#interior_fittings-interior_door_casing')?.checked
    ) {
      laborCost += 500
      materialCost += 250
    }

    // Outer Door Casing Replacement
    if (
      document.querySelector('#interior_fittings-exterior_door_casing')?.checked
    ) {
      laborCost += 500
      materialCost += 250
    }

    // Door Frame Replacement
    if (
      document.querySelector('#interior_fittings-doorframe_replacement')
        ?.checked
    ) {
      laborCost += 1000
      materialCost += 1000
    }

    // Window Repainting
    if (
      document.querySelector('#interior_fittings-window_repainting')?.checked
    ) {
      laborCost += 500
      materialCost += 250
    }

    // Niches without Spotlight
    const nichesCount =
      parseInt(
        document.querySelector('#interior_fittings-niches_count')?.value
      ) || 0
    const nichesPrice =
      parseFloat(
        document.querySelector('#interior_fittings-niches_price')?.value
      ) || 0
    if (nichesCount > 0) {
      laborCost += nichesCount * nichesPrice
    }

    return { laborCost, materialCost }
  }

  function calculateTilingAndPaintingCosts () {
    let laborCost = 0
    let materialCost = 0

    // Floor Tile Size Deviation
    const floorTileDeviation =
      document.querySelector('#tiles_and_painting-floor_tile_deviation')
        ?.value || ''
    if (floorTileDeviation) {
      // Assuming a fixed cost for deviation - would need actual values from J94
      laborCost += 500
      materialCost += 500
    }

    // Wall Tile Size Deviation
    const wallTileDeviation =
      document.querySelector('#tiles_and_painting-wall_tile_deviation')
        ?.value || ''
    if (wallTileDeviation) {
      // Assuming a fixed cost for deviation - would need actual values from J96
      laborCost += 500
      materialCost += 500
    }

    // Grout Colors
    const groutColors =
      parseInt(
        document.querySelector('#tiles_and_painting-grout_colors')?.value
      ) || 0
    const groutColorsPrice =
      parseFloat(
        document.querySelector('#tiles_and_painting-grout_colors_price')?.value
      ) || 0
    if (groutColors > 1) {
      laborCost += (groutColors - 1) * groutColorsPrice
      materialCost += (groutColors - 1) * groutColorsPrice
    }

    // Ceiling Painting Time
    const ceilingHours =
      parseFloat(
        document.querySelector('#tiles_and_painting-ceiling_painting_hours')
          ?.value
      ) || 0
    const ceilingPrice =
      parseFloat(
        document.querySelector('#tiles_and_painting-ceiling_painting_price')
          ?.value
      ) || 0
    if (ceilingHours > 0) {
      laborCost += ceilingHours * ceilingPrice
    }

    // Wall Painting Time
    const wallHours =
      parseFloat(
        document.querySelector('#tiles_and_painting-wall_painting_hours')?.value
      ) || 0
    const wallPrice =
      parseFloat(
        document.querySelector('#tiles_and_painting-wall_painting_price')?.value
      ) || 0
    if (wallHours > 0) {
      laborCost += wallHours * wallPrice
    }

    // Wall Painting Material
    const wallArea =
      parseFloat(
        document.querySelector('#tiles_and_painting-wall_area')?.value
      ) || 0
    const wallAreaPrice =
      parseFloat(
        document.querySelector('#tiles_and_painting-wall_area_price')?.value
      ) || 0
    if (wallArea > 0) {
      materialCost += wallArea * wallAreaPrice
    }

    // Add ceiling painting material calculation that was missing
    if (document.querySelector('#tiles_and_painting-paint_ceiling')?.checked) {
      const ceilingArea =
        parseFloat(
          document.querySelector('#tiles_and_painting-ceiling_area')?.value
        ) || 0
      const ceilingAreaPrice =
        parseFloat(
          document.querySelector('#tiles_and_painting-ceiling_area_price')
            ?.value
        ) || 0
      materialCost += ceilingArea * ceilingAreaPrice
    }

    return { laborCost, materialCost }
  }

  function calculateWasteAndCleanupCosts () {
    let otherCosts = 0

    // Construction Bag
    const bagCount =
      parseInt(
        document.querySelector('#tiles_and_painting-construction_bag')?.value
      ) || 0
    const bagPrice = 1500 // Assuming a fixed price per bag
    otherCosts += bagCount * bagPrice

    // Basic waste costs
    const floorArea =
      parseFloat(
        document.querySelector('#bathroom_details-floor_area')?.value
      ) || 0
    otherCosts += 5000 + floorArea * 200

    return otherCosts
  }

  function calculateExtraItemsCosts () {
    let laborCost = 0
    let materialCost = 0
    let otherCost = 0

    // Find all extra items input rows
    const extraItemRows = document.querySelectorAll(
      '[id^="additional_notes-extra_items-"][id$="-item"]'
    )

    extraItemRows.forEach(itemInput => {
      // Extract the index from the ID (e.g., "additional_notes-extra_items-0-item" -> "0")
      const index = itemInput.id.match(
        /additional_notes-extra_items-(\d+)-item/
      )[1]

      // Get the corresponding cost input
      const costInput = document.querySelector(
        `#additional_notes-extra_items-${index}-cost`
      )

      if (itemInput.value && costInput?.value) {
        const itemName = itemInput.value.toLowerCase()
        const cost = parseFloat(costInput.value) || 0

        if (cost > 0) {
          // Labor related keywords
          const laborKeywords = [
            'arbete',
            'labor',
            'montering',
            'installation',
            'service'
          ]
          // Material related keywords
          const materialKeywords = [
            'material',
            'utrustning',
            'equipment',
            'supplies',
            'parts'
          ]
          // Other/waste related keywords
          const otherKeywords = [
            'avfall',
            'waste',
            'transport',
            'frakt',
            'freight',
            'avgift',
            'fee'
          ]

          // Categorize cost based on item name
          if (laborKeywords.some(keyword => itemName.includes(keyword))) {
            laborCost += cost
          } else if (
            materialKeywords.some(keyword => itemName.includes(keyword))
          ) {
            materialCost += cost
          } else if (
            otherKeywords.some(keyword => itemName.includes(keyword))
          ) {
            otherCost += cost
          } else {
            // Default to material cost if no category is detected
            materialCost += cost
          }
        }
      }
    })

    return { laborCost, materialCost, otherCost }
  }

  // Update all calculations
  function updatePricePreview () {
    // Calculate all options
    updateMainOption()
    updateOption1()
    updateOption2()
  }

  // Calculate and update the main option
  function updateMainOption () {
    // Calculate all cost components
    const seasonCost = calculateSeasonCost()
    const generalCosts = calculateGeneralConditionsCosts()
    const accessibility = calculateAccessibilityCosts()
    const protection = calculateFloorProtectionCosts()
    const dimensionCosts = calculateBathroomDimensionCosts()
    const layoutCosts = calculateLayoutModificationCosts()
    const plumbingCosts = calculatePlumbingCosts()
    const electricalCosts = calculateElectricalCosts()
    const fixturesCosts = calculateFixturesCosts()
    const tilingCosts = calculateTilingAndPaintingCosts()
    const wasteCosts = calculateWasteAndCleanupCosts()
    const extraItemsCosts = calculateExtraItemsCosts()

    // Calculate totals for each category
    const totalLabor =
      seasonCost +
      generalCosts +
      accessibility.laborCost +
      protection.laborCost +
      dimensionCosts.basicLabor +
      layoutCosts.laborCost +
      plumbingCosts.laborCost +
      electricalCosts.laborCost +
      fixturesCosts.laborCost +
      tilingCosts.laborCost +
      extraItemsCosts.laborCost

    const totalMaterials =
      protection.materialCost +
      dimensionCosts.basicMaterials +
      layoutCosts.materialCost +
      plumbingCosts.materialCost +
      electricalCosts.materialCost +
      fixturesCosts.materialCost +
      tilingCosts.materialCost +
      extraItemsCosts.materialCost

    const totalOtherCosts =
      accessibility.otherCosts + wasteCosts + extraItemsCosts.otherCost

    // Apply discount - 1000 SEK on labor and material
    const laborAfterDiscount = totalLabor - 1000
    const materialAfterDiscount = totalMaterials - 1000
    const otherAfterDiscount = totalOtherCosts - 1000

    // Calculate ROT deduction (30% of labor cost, max 50,000 SEK)
    const rotDeduction = Math.min(laborAfterDiscount * 0.3, 50000)

    // Calculate final costs to be paid by customer
    const laborPaidByCustomer = laborAfterDiscount - rotDeduction
    const materialPaidByCustomer = materialAfterDiscount
    const otherPaidByCustomer = otherAfterDiscount

    // Calculate total cost
    const totalCost =
      laborPaidByCustomer + materialPaidByCustomer + otherPaidByCustomer

    // Update UI
    safelyUpdateElement(
      '#laborCostAfterRot',
      formatCurrency(laborPaidByCustomer)
    )
    safelyUpdateElement('#materialCost', formatCurrency(materialPaidByCustomer))
    safelyUpdateElement('#wasteCost', formatCurrency(otherPaidByCustomer))
    safelyUpdateElement('#discount', formatCurrency(3000)) // Total discount (1000 from each category)
    safelyUpdateElement('#totalCost', formatCurrency(totalCost))
    safelyUpdateElement('#rotDeduction', formatCurrency(rotDeduction))

    // Debug logging
    console.log('MAIN OPTION CALCULATION:', {
      totalLabor,
      totalMaterials,
      totalOtherCosts,
      laborAfterDiscount,
      materialAfterDiscount,
      otherAfterDiscount,
      rotDeduction,
      laborPaidByCustomer,
      materialPaidByCustomer,
      otherPaidByCustomer,
      totalCost,
      extraItems: extraItemsCosts
    })
  }

  // Calculate and update Option 1
  function updateOption1 () {
    // Option 1: Simpler renovation (Totalrenovering i enklare form)
    const floorArea =
      parseFloat(
        document.querySelector('#bathroom_details-floor_area')?.value
      ) || 0

    // Get extra items costs
    const extraItemsCosts = calculateExtraItemsCosts()

    // Base costs for Option 1
    let laborCost = 24500
    let materialCost = 20000
    let otherCosts = 4000

    // Scale costs based on floor area
    laborCost += floorArea * 800
    materialCost += floorArea * 1500
    otherCosts += floorArea * 150

    // Add extra items costs
    laborCost += extraItemsCosts.laborCost
    materialCost += extraItemsCosts.materialCost
    otherCosts += extraItemsCosts.otherCost

    // Apply discount - same as main option
    const laborAfterDiscount = laborCost - 1000
    const materialAfterDiscount = materialCost - 1000
    const otherAfterDiscount = otherCosts - 1000

    // Calculate ROT deduction (30% of labor cost, max 50,000 SEK)
    const rotDeduction = Math.min(laborAfterDiscount * 0.3, 50000)

    // Calculate final costs
    const laborPaidByCustomer = laborAfterDiscount - rotDeduction
    const materialPaidByCustomer = materialAfterDiscount
    const otherPaidByCustomer = otherAfterDiscount

    // Calculate total cost
    const totalCost =
      laborPaidByCustomer + materialPaidByCustomer + otherPaidByCustomer

    // Update Option 1 section - safely access DOM elements
    safelyUpdateElement(
      '#laborCostAfterRotOption1',
      formatCurrency(laborPaidByCustomer)
    )
    safelyUpdateElement(
      '#materialCostOption1',
      formatCurrency(materialPaidByCustomer)
    )
    safelyUpdateElement(
      '#wasteCostOption1',
      formatCurrency(otherPaidByCustomer)
    )
    safelyUpdateElement('#discountOption1', formatCurrency(3000)) // Total discount
    safelyUpdateElement('#totalCostOption1', formatCurrency(totalCost))

    // Debug logging for verification
    console.log('OPTION 1 CALCULATION:', {
      laborCost,
      materialCost,
      otherCosts,
      laborAfterDiscount,
      materialAfterDiscount,
      otherAfterDiscount,
      rotDeduction,
      laborPaidByCustomer,
      materialPaidByCustomer,
      otherPaidByCustomer,
      totalCost,
      extraItems: extraItemsCosts
    })
  }

  // Calculate and update Option 2
  function updateOption2 () {
    // Option 2: Water-heated floor (Vattenburen golvvärme)
    const floorArea =
      parseFloat(
        document.querySelector('#bathroom_details-floor_area')?.value
      ) || 0

    // Get extra items costs
    const extraItemsCosts = calculateExtraItemsCosts()

    // Base costs for Option 2
    let laborCost = 38500
    let materialCost = 30000
    let otherCosts = 6000

    // Scale costs based on floor area
    laborCost += floorArea * 1200
    materialCost += floorArea * 2500
    otherCosts += floorArea * 250

    // Add extra items costs
    laborCost += extraItemsCosts.laborCost
    materialCost += extraItemsCosts.materialCost
    otherCosts += extraItemsCosts.otherCost

    // Apply discount - same as main option
    const laborAfterDiscount = laborCost - 1000
    const materialAfterDiscount = materialCost - 1000
    const otherAfterDiscount = otherCosts - 1000

    // Calculate ROT deduction (30% of labor cost, max 50,000 SEK)
    const rotDeduction = Math.min(laborAfterDiscount * 0.3, 50000)

    // Calculate final costs
    const laborPaidByCustomer = laborAfterDiscount - rotDeduction
    const materialPaidByCustomer = materialAfterDiscount
    const otherPaidByCustomer = otherAfterDiscount

    // Calculate total cost
    const totalCost =
      laborPaidByCustomer + materialPaidByCustomer + otherPaidByCustomer

    // Update Option 2 section - safely access DOM elements
    safelyUpdateElement(
      '#laborCostAfterRotOption2',
      formatCurrency(laborPaidByCustomer)
    )
    safelyUpdateElement(
      '#materialCostOption2',
      formatCurrency(materialPaidByCustomer)
    )
    safelyUpdateElement(
      '#wasteCostOption2',
      formatCurrency(otherPaidByCustomer)
    )
    safelyUpdateElement('#discountOption2', formatCurrency(3000)) // Total discount
    safelyUpdateElement('#totalCostOption2', formatCurrency(totalCost))

    // Debug logging for verification
    console.log('OPTION 2 CALCULATION:', {
      laborCost,
      materialCost,
      otherCosts,
      laborAfterDiscount,
      materialAfterDiscount,
      otherAfterDiscount,
      rotDeduction,
      laborPaidByCustomer,
      materialPaidByCustomer,
      otherPaidByCustomer,
      totalCost,
      extraItems: extraItemsCosts
    })
  }

  // Helper function to safely update DOM elements
  function safelyUpdateElement (selector, value) {
    const element = document.querySelector(selector)
    if (element) {
      element.textContent = value
    }
  }

  // Add event listeners for price-affecting inputs
  const priceAffectingInputs = document.querySelectorAll('.price-affecting')
  priceAffectingInputs.forEach(input => {
    input.addEventListener('change', debounce(updatePricePreview, 300))
    input.addEventListener('input', debounce(updatePricePreview, 300))
  })

  // Initial calculation
  updatePricePreview()
})

// Helper functions
function formatCurrency (amount) {
  return new Intl.NumberFormat('sv-SE', {
    style: 'currency',
    currency: 'SEK'
  }).format(amount)
}

function debounce (func, wait) {
  let timeout
  return function executedFunction (...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// Export functions for testing
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    formatCurrency,
    debounce
  }
}
